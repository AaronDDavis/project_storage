"""
URL configurations for public/renter-facing Space listings.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:space_id>/', views.SpaceDetailView.as_view(), name = 'space_details'),
    
    path('search/', views.SpaceListView.as_view(), name = 'search_space'),
]
