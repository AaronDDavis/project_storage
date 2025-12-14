"""
Admin configuration for CustomUser.

This module integrates the custom `nric_fin` and `role` fields into the  standard Django User admin interface, ensuring administrators can manage these attributes during user creation and editing.
"""
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """
    Custom administration interface configuration for the CustomUser model.

    This class extends the standard `UserAdmin` provided by Django, which
    ensures that the core fields (e.g., username, email, permissions) are
    managed correctly. Its primary purpose is to integrate the custom fields (`nric_fin` and `role`) into both the change and add forms in the admin.

    Attributes:
        fieldsets (tuple): Controls the fields displayed on the **change** form for an existing user, organizing them into logical groupings.
        add_fieldsets (tuple): Controls the fields displayed on the **add** form when creating a **new** user.

    Args:
        UserAdmin: Inherits all default fields, list display, and security checks for managing users.
    """
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["nric_fin", "role"]}),)
    
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["nric_fin", "role"]}),)


admin.site.register(CustomUser, CustomUserAdmin)
