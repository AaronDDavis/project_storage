"""
URL configurations for Renter-facing Installation Requests.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:installation_request_id>/', views.InstallationRequestDetailView.as_view(), name = 'installation_request_details'),
    
    path('all/', views.InstallationRequestListView.as_view(), name = 'installation_request_list'),
    
    path("new/", views.InstallationRequestCreateView.as_view(), name='create_installation_request'),
    
    # Action to finalize a request and generate a Space object
    path("to_space/<int:installation_request_id>/", views.convert_request_to_space , name='installation_request_to_space'),
]
