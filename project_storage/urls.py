"""
Root URL configuration.

Delegates traffic to specific application modules, separating standard user workflows from custom administrative tools.
"""
from django.urls import path, include

urlpatterns = [
    # Custom Administrative Tools
    path('admin/space/', include('listings.admin_urls')),
    path('admin/installation_request/', include('prelistings.admin_urls')),

    # Application Workflows
    path('space/', include('listings.urls')),
    path('installation_request/', include('prelistings.urls')),
    path('bookings/', include('bookings.urls')),
    path('user/', include('users.urls')),
]
