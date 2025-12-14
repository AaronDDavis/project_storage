"""
Request handlers for the installation request workflow.
"""
from django.urls import reverse_lazy
from .models import InstallationRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .services import InstallationRequestService, InstallationRequestStateService
from .forms import InstallationRequestForm
from listings.models import LOCATION_DEFS, Location, Space, SHELF_LENGTH, SHELF_WIDTH, SHELF_HEIGHT
import json
from django.shortcuts import get_object_or_404, redirect
from .exceptions import InstallationRequestError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_POST


class InstallationRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Lists installation requests submitted by the current renter.
    """
    model = InstallationRequest
    template_name = 'prelistings/installation_request_list.html'
    context_object_name = 'installation_requests'

    def test_func(self):
        """Restricts access to Renters."""
        return self.request.user.is_renter
    
    def get_queryset(self):
        return InstallationRequestService.get_installation_requests(renter = self.request.user)
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['Status'] = InstallationRequest.Status
        return context_data


class InstallationRequestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Handles submission of new installation requests.
    """
    model = InstallationRequest
    form_class = InstallationRequestForm
    template_name = 'prelistings/installation_request_form.html'
    success_url = reverse_lazy('installation_request_list')

    def test_func(self):
        """Restricts access to Renters."""
        return self.request.user.is_renter
    
    def get_context_data(self, **kwargs):
        """Passes location choices and pricing map (JSON) to the frontend."""
        context_data = super().get_context_data(**kwargs)
        context_data['LOCATION_CHOICES'] = LOCATION_DEFS
        context_data['LOCATION_PRICES'] = json.dumps({code: float(price) for code, _, price in LOCATION_DEFS})
        return context_data
    
    def form_valid(self, form):
        form.instance.renter = self.request.user

        # Create the Location object explicitly before saving the Request
        location = Location()
        location.area = self.request.POST.get('location-area')
        location.address = self.request.POST.get('location-address')
        location.load_price()
        location.save()

        form.instance.location = location
        form.instance.price_per_day = Space.get_price(location)
        
        response = super().form_valid(form)
        return response


class InstallationRequestDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Displays details of a specific installation request.
    """
    model = InstallationRequest
    template_name = 'prelistings/installation_request_details.html'
    pk_url_kwarg = 'installation_request_id'

    def test_func(self):
        """Restricts access to Renters."""
        return self.request.user.is_renter
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['installation_request'] = get_object_or_404(InstallationRequest, pk=self.kwargs['installation_request_id'])
        installation_request = context_data['installation_request']
        
        context_data['shelf_length'] = SHELF_LENGTH
        context_data['shelf_width'] = SHELF_WIDTH
        context_data['shelf_height'] = SHELF_HEIGHT
        
        try:
            context_data['total_shelves'] = InstallationRequestService.get_total_shelves(installation_request)
        except InstallationRequestError:
            context_data['total_shelves'] = 0

        return context_data


class AdminInstallationRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Lists all installation requests for administrator review.
    """
    model = InstallationRequest
    template_name = 'admin/admin_installation_request_list.html'
    context_object_name = 'installation_requests'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self, **kwargs):
        installation_requests = InstallationRequestService.get_installation_requests().order_by('id')

        search_status = self.request.GET.get('search-status')

        if InstallationRequestStateService.is_valid_status(search_status):
            installation_requests = installation_requests.filter(status = search_status)

        return installation_requests
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        
        context_data['request_status'] = InstallationRequest.Status
        context_data['current_status'] = self.request.GET.get('search-status', 'ALL')
        
        return context_data


class AdminInstallationRequestDetaiView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Displays request details for admins and handles shelf configuration.
    """
    model = InstallationRequest
    template_name = 'admin/admin_installation_request_detail.html'
    pk_url_kwarg = 'installation_request_id'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['status'] = InstallationRequest.Status
        context_data['installation_request'] = get_object_or_404(InstallationRequest, pk=self.kwargs['installation_request_id'])
        installation_request = context_data['installation_request']

        context_data['shelf_length'] = SHELF_LENGTH
        context_data['shelf_width'] = SHELF_WIDTH
        context_data['shelf_height'] = SHELF_HEIGHT
        
        context_data['total_shelves'] = InstallationRequestService.get_total_shelves(installation_request)
        
        return context_data
    
    def post(self, request, *args, **kwargs):
        """Handles the configuration of rack/shelf numbers by the Admin."""
        installation_request = self.get_object()
    
        installation_request.num_rack = int(request.POST.get('shelf-height-num'))
        installation_request.num_shelves_per_rack = int(request.POST.get('shelf-length-num'))
        installation_request.save()

        return redirect(
            'admin_installation_request_details',
            installation_request_id = installation_request.id
        )


@login_required
@user_passes_test(lambda user: user.is_renter)
def convert_request_to_space(request, installation_request_id: int):
    """
    Finalizes a completed request by converting it into a Space.
    """
    installation_request = get_object_or_404(InstallationRequest, pk = installation_request_id)
    try:
        # Atomic conversion handled by the Service layer
        space = InstallationRequestService.convert_to_space(installation_request)
        messages.success(
            request,
            f"Successfully created space at {space.location.get_area_display()}"
        )
    except InstallationRequestError as e:
        messages.error(
            request,
            e.message
        )
    return redirect('dashboard')


@login_required
@require_POST
def update_installation_request_status(request, installation_request_id, new_status):
    """
    Handles status transitions (e.g., Approve, Reject) for requests.
    """
    if not request.user.is_superuser:
        return redirect('admin_installation_request_list')
    
    installation_request = get_object_or_404(InstallationRequest, pk = installation_request_id)

    try:
        InstallationRequestStateService.transition(installation_request, new_status)
        messages.success(request, f"Successfully updated!\nRequest at {installation_request.location.get_area_display()} is now '{installation_request.get_status_display()}'")
    except InstallationRequestError as e:
        messages.error(request, e.message)
    
    return redirect('admin_installation_request_list')
