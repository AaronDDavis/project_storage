"""
Request handlers for creating and viewing bookings.
"""
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Booking
from listings.models import Space, SHELF_LENGTH, SHELF_WIDTH, SHELF_HEIGHT
from .forms import BookingForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView
from .services import BookingService, DateMgr, BookingFormService

# Create your views here.
class BookingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Handles the creation of new bookings by Lessees.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        """Ensures only Lessees can create bookings."""
        return self.request.user.is_lessee
    
    def get_context_data(self, **kwargs):
        """Injects space details and shelf dimensions into the template."""
        context_data = super().get_context_data(**kwargs)
        context_data['space'] = get_object_or_404(Space, pk=self.kwargs['space_id'])
        context_data['num_shelves_occupied'] = self.kwargs['num_shelves']

        context_data['shelf_length'] = SHELF_LENGTH
        context_data['shelf_width'] = SHELF_WIDTH
        context_data['shelf_height'] = SHELF_HEIGHT

        return context_data
    
    def form_valid(self, form):
        space = get_object_or_404(Space, pk=self.kwargs['space_id'])

        # Auto-assign a rack that meets the capacity requirements
        form.instance.rack = BookingFormService.get_rack(space, self.kwargs['num_shelves'])
        form.instance.lessee = self.request.user
        
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        # Calculate final price before saving (Days * Rate * Shelves)
        num_days = DateMgr.get_total_days(start_date, end_date)
        form.instance.num_shelves_occupied = self.kwargs['num_shelves']
        form.instance.total_price = num_days * space.price_per_day * form.instance.num_shelves_occupied

        return super().form_valid(form)


def cancel_booking(request, booking_id):
    """Cancels an existing booking."""
    booking = get_object_or_404(Booking, pk = booking_id)
    
    if BookingService.cancel_booking(booking, request.user):
        messages.success(
                request,
            f"Successfully cancelled Booking at {booking.rack.space.location.get_area_display()} from {booking.start_date} to {booking.end_date}")
        return redirect('dashboard')


class BookingDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Displays detailed information about a specific booking.
    """
    model = Booking
    template_name = 'bookings/booking_details.html'
    pk_url_kwarg = 'booking_id'

    def test_func(self):
        """Ensures only Lessees can view their own bookings."""
        return self.request.user.is_lessee
    
    def get_context_data(self, **kwargs):
        """Calculates duration and per-shelf pricing for display."""
        context_data = super().get_context_data(**kwargs)
        context_data['booking'] = booking = get_object_or_404(Booking, pk=self.kwargs['booking_id'])
        context_data['total_days'] = BookingService.get_total_days(booking)
        context_data['price_per_day'] = BookingService.get_price_per_day(booking)

        # Pass status enums for template logic
        context_data['active_status'] = Booking.Status.ACTIVE
        context_data['booked_status'] = Booking.Status.BOOKED
        context_data['past_status'] = Booking.Status.PAST
        context_data['cancelled_status'] = Booking.Status.CANCELLED

        return context_data
