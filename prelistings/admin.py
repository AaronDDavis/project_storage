"""
Admin configuration for Installation Requests.
"""
from django.contrib import admin
from .models import InstallationRequest

admin.site.register(InstallationRequest)