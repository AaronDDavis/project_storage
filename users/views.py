"""
Request handlers for Authentication and Dashboard routing.
"""
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomLoginForm
from django.urls import reverse_lazy
from listings.services import SpaceService
from bookings.models import Booking
from bookings.services import BookingStateService
from django.db.models import Count, Q
from django.contrib.auth.views import LoginView


class SignUpView(CreateView):
    """
    Handles user registration.

    Redirects to the login page upon success.
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def view_dashboard(request):
    """
    Renders the dashboard corresponding to the authenticated user's role.

    Args:
        request: The incoming HttpRequest.

    Returns:
        HttpResponse: The role-specific dashboard template.
    """
    if request.user.is_superuser:
        return redirect('admin_space_list')
        
    elif request.user.is_renter:
        renter_spaces = SpaceService.get_spaces(renter=request.user)
        
        annotated_spaces = renter_spaces.annotate(
            booked_shelves=Count('rack__shelf',
                filter=Q(rack__shelf__is_available=False),
                distinct=True)
            )
            
        return render(request, 'dashboards/renter_dashboard.html', {'spaces': annotated_spaces})
        
    elif request.user.is_lessee:
        bookings = Booking.objects.filter(lessee=request.user)
        
        for booking in bookings:
            BookingStateService.update_status(booking)
            
        active_bookings_queryset = bookings.filter(
            Q(status='BOOKED') | Q(status='ACTIVE')
            ).order_by('-end_date')

        past_bookings_queryset = bookings.filter(
            Q(status='PAST') | Q(status='CANCELLED')
            ).order_by('-end_date')
            
        return render(
            request,
            'dashboards/lessee_dashboard.html',
            {
                'active_bookings': active_bookings_queryset,
                'past_bookings': past_bookings_queryset,
                'active_status': Booking.Status.ACTIVE,
                'past_status': Booking.Status.PAST,
            }
        )


class CustomLoginView(LoginView):
    """
    Handles user login using the custom authentication form.
    """
    authentication_form = CustomLoginForm


def view_profile(request):
    """
    Renders the read-only user profile page.
    """
    return render(request, 'profiles/profile.html', {'user': request.user})
