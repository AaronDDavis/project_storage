"""
Request handlers for Space listings and management.

Handles public listing searches (delegating availability logic to SpaceService) and specific views for Renters (Space Details) and Admins (Approval queues).
"""

from .models import Space
from .constants import SHELF_LENGTH, SHELF_HEIGHT, SHELF_WIDTH
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .services import SpaceStateService, SpaceService, SpaceLayoutService
from .exceptions import SpaceStateError
from bookings.services import BookingService
from bookings.models import Booking


class SpaceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Handles listing available Space objects. Accessible only by Lessees.

    This view handles form submissions (search parameters) and delegates the complex availability calculation and filtering to the SpaceService.
    """
    model = Space
    template_name = 'listings/space_list.html'
    context_object_name = 'available_spaces'

    def test_func(self):
        """
        Enforces authorization: only users with the 'LESSEE' role can access this list view.
        """
        return self.request.user.is_lessee
    
    def get_queryset(self):
        """
        Retrieves the QuerySet of spaces available for booking based on URL query parameters.

        It extracts search parameters from the request and passes them directly to the SpaceService for processing.

        Returns:
            QuerySet: A filtered QuerySet of Space objects that are currently available.
        """
        # Retrieve search parameters
        search_location = self.request.GET.get('search-location')
        search_length = int(self.request.GET.get('search-length', 1))
        search_width = int(self.request.GET.get('search-width', 1))
        search_height = int(self.request.GET.get('search-height', 1))

        # Delegate the complex filtering logic to the SpaceService.
        return SpaceService.get_available_spaces(search_location, search_length, search_width, search_height)


class SpaceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Handles the display of detailed information for a single Space object.
    Accessible only by Renters.
    """
    model = Space
    template_name = 'listings/space_details.html'
    pk_url_kwarg = 'space_id'

    def test_func(self):
        """
        Enforces authorization: only users with the 'RENTER' role can view the details.
        """
        return self.request.user.is_renter
    
    def get_context_data(self, **kwargs):
        """
        Adds contextual data, including the shelf layout map, related bookings, and fixed shelf dimensions, to the template context.

        Returns:
            dict: The context dictionary passed to the template.
        """
        context_data = super().get_context_data(**kwargs)

        context_data['space'] = get_object_or_404(Space, pk=self.kwargs['space_id'])
        space = context_data['space']
        
        # Retrieve the availability map for display purposes from the SpaceLayoutService.
        context_data['shelf_layout'] = SpaceLayoutService.get_shelf_layout(space)

        # Fetch and categorize all related bookings via the BookingService.
        context_data['active_bookings'] = BookingService.get_bookings(space = space, status = Booking.Status.ACTIVE)
        context_data['upcoming_bookings'] = BookingService.get_bookings(space = space, status = Booking.Status.BOOKED)
        context_data['past_bookings'] = BookingService.get_bookings(space = space, status = Booking.Status.PAST)

        context_data['shelf_length'] = SHELF_LENGTH
        context_data['shelf_width'] = SHELF_WIDTH
        context_data['shelf_height'] = SHELF_HEIGHT
        context_data['total_shelves'] = space.total_shelves

        return context_data


class AdminSpaceListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Handles the list view of all Space objects for administrative review.
    Accessible only by superusers. Allows filtering by space status.
    """
    model = Space
    template_name = 'admin/admin_space_list.html'
    context_object_name = 'spaces'

    def test_func(self):
        """
        Enforces authorization: only superusers can access this view.
        """
        return self.request.user.is_superuser
    
    def get_queryset(self, **kwargs):
        """
        Retrieves all Space objects, optionally filtering by status from GET parameters.

        Returns:
            QuerySet: A QuerySet of all Space objects, ordered by ID.
        """
        spaces = SpaceService.get_spaces().order_by('id')

        search_status = self.request.GET.get('search-status')

        # Use the SpaceStateService to ensure the status provided is a valid code before filtering.
        if SpaceStateService.is_valid_status(search_status):
            spaces = spaces.filter(status = search_status)

        return spaces
    
    def get_context_data(self, **kwargs):
        """
        Adds necessary data for the administrative filter form, including all possible status choices.

        Returns:
            dict: The context dictionary passed to the template.
        """
        context_data = super().get_context_data(**kwargs)
        
        context_data['statuses'] = Space.Status.choices
        
        context_data['current_status'] = self.request.GET.get('search-status', 'ALL')
        
        return context_data


class AdminSpaceDetaiView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Handles the detailed view of a single Space for administrative purposes.
    Accessible only by superusers. Displays layout and allows status changes.
    """
    model = Space
    template_name = 'admin/admin_space_detail.html'
    pk_url_kwarg = 'space_id'

    def test_func(self):
        """
        Enforces authorization: only superusers can access this view.
        """
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        Adds contextual data for administrative display, including shelf layout and dimensional constants.

        Returns:
            dict: The context dictionary passed to the template.
        """
        context_data = super().get_context_data(**kwargs)

        context_data['status'] = Space.Status
        
        context_data['space'] = get_object_or_404(Space, pk=self.kwargs['space_id'])
        space = context_data['space']

        # Retrieve the shelf availability map.
        context_data['shelf_layout'] = SpaceLayoutService.get_shelf_layout(space)
        
        context_data['shelf_length'] = SHELF_LENGTH
        context_data['shelf_width'] = SHELF_WIDTH
        context_data['shelf_height'] = SHELF_HEIGHT
        context_data['total_shelves'] = space.total_shelves

        return context_data


@login_required
@require_POST
def update_space_status(request, space_id, new_status):
    """
    Function-based view to handle POST requests for changing a Space object's status.
    Requires login and is restricted to superusers.

    Args:
        request (HttpRequest): The incoming request object.
        space_id (int): The primary key of the Space object to update.
        new_status (str): The target status code.

    Returns:
        HttpResponse: A redirect response, either back to the admin list view with a success message or with an error message if transition fails.
    """
    # Only superusers can execute this function.
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    space = get_object_or_404(Space, pk = space_id)

    try:
        # Delegate the state transition logic and validation to the SpaceStateService.
        SpaceStateService.transition(space, new_status)

        messages.success(request, f"Successfully updated!\nSpace at {space.location.get_area_display()} is now {space.get_status_display()}")

    except SpaceStateError as e:
        messages.error(request, e.message)
    
    return redirect('admin_space_list')
