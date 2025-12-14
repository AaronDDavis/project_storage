"""
URL configurations for internal Space management (Custom Admin Dashboard).
"""
from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.AdminSpaceListView.as_view(), name = 'admin_space_list'),
    
    path('<int:space_id>/', views.AdminSpaceDetaiView.as_view(), name = 'admin_space_details'),
    
    # State transition endpoint (e.g., Approve/Reject space)
    path('<int:space_id>/<str:new_status>/', views.update_space_status, name = 'update_space_status'),
]
