"""
URL configurations for Authentication and User Profiles.
"""
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name='signup'),
    
    # Central routing view (redirects to Renter vs Lessee dashboard)
    path('dashboard/', views.view_dashboard, name='dashboard'),
    
    path('profile/', views.view_profile, name='profile'),
    path('login/', views.CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
]
