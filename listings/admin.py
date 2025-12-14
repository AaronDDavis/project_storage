"""
Admin configuration for Inventory management.

Customizes the display of Spaces, Racks, and Shelves using Inlines to visualize the parent-child hierarchy. Includes custom actions for bulk status updates (e.g., Approve Spaces).
"""

from django.contrib import admin
from .models import Space, Shelf, Rack
from django.db.models import QuerySet

class ShelfInline(admin.TabularInline):
    """
    Defines the inline appearance of Shelf objects when editing a parent Rack object.

    Uses `TabularInline` for a compact, spreadsheet-like display.
    """
    model = Shelf

class RackAdmin(admin.ModelAdmin):
    """
    Customizes the Django Admin interface for the Rack model.
    """
    # Includes Shelf objects directly within the Rack editing screen, enforcing
    # the one-to-many relationship visually.
    inlines = [ShelfInline]

class RackInline(admin.TabularInline):
    """
    Defines the inline appearance of Rack objects when editing a parent Space object.

    Uses `TabularInline` for compact display of Racks within a Space.
    """
    model = Rack

class SpaceAdmin(admin.ModelAdmin):
    """
    Customizes the Django Admin interface for the Space model, adding
    relationship inlines, display columns, filtering options, and custom actions.
    """
    # Includes Rack objects directly within the Space editing screen.
    inlines = [RackInline]
    
    # Specifies the fields shown on the list view page.
    list_display = ('status', )
    
    # Enables filtering in the sidebar based on the `status` field.
    list_filter = ('status', )

    def approve_spaces(spaces: QuerySet):
        """
        Custom administrative action to bulk update the status of selected Space objects to 'APPROVED'.

        Args:
            spaces (QuerySet): The QuerySet of Space objects selected by the administrator.

        Side Effects:
            Performs a bulk database update on the 'status' field for the selected objects.
        """
        # Performs a single bulk SQL update query for efficiency.
        spaces.update(status = 'APPROVED')

    # Registers the custom function `approve_spaces` as an available action on the list view.
    actions = [approve_spaces]


# Registers the customized Admin classes with the Django Admin site.
admin.site.register(Rack, RackAdmin)
admin.site.register(Space, SpaceAdmin)
