"""
URL configurations for internal Installation Request management.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.AdminInstallationRequestListView.as_view(), name = 'admin_installation_request_list'),
    
    path('<int:installation_request_id>/', views.AdminInstallationRequestDetaiView.as_view(), name = 'admin_installation_request_details'),
    
    path('<int:installation_request_id>/<str:new_status>/', views.update_installation_request_status, name = 'update_installation_request_status'),
]
