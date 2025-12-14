"""
URL configurations for the Booking workflow.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Creation flow requires target Space ID and shelf quantity
    path("book/<int:space_id>/<int:num_shelves>/", views.BookingCreateView.as_view(), name='book_space'),
    
    path("details/<int:booking_id>/", views.BookingDetailsView.as_view(), name='booking_details'),
    
    path("cancel/<int:booking_id>/", views.cancel_booking, name='cancel_booking'),
]
