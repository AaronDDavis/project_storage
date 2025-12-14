"""
Database models representing the physical inventory hierarchy (Location -> Space -> Rack -> Shelf).
"""

from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _
from .constants import SHELF_LENGTH, SHELF_WIDTH, SHELF_HEIGHT, LOCATION_DEFS

class Location(models.Model):
    """
    Represents a geographic location and its associated base rate.

    Attributes:
        area (str): Short code for the planning area.
        address (str): Physical address.
        price_per_day (Decimal): Base daily price for this location.
    """
    # The choices for 'area' are generated dynamically from the predefined list in constants.py, using only the code and the full name.
    area = models.CharField(
        max_length = 3, 
        choices = [(code, name) for code, name, _ in LOCATION_DEFS]
    )

    address = models.CharField(max_length = 200)

    # Price per day of a shelf in a particular location
    price_per_day = models.DecimalField(max_digits = 4, decimal_places = 2, default = 1.00)

    def load_price(self):
        """
        Updates price_per_day based on the instance's area code.
        """
        # Search LOCATION_DEFS for a matching area code.
        val = [data for data in LOCATION_DEFS if data[0] == self.area]
        
        self.price_per_day = val[0][2] if len(val) == 1 else 0


class EnvironmentConditions(models.TextChoices):
    """Available environmental conditions for a Space."""
    AC = 'AC', _('Air-conditioned (Indoor)')
    INDOOR = 'INDOOR', _('Indoor (Non Air-conditioned)')
    OUTDOOR = 'OUTDOOR', _('Outdoor (Sheltered)')


class Space(models.Model):
    """
    Represents a rentable storage unit composed of multiple racks.
    """

    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        ON_HOLD = 'ON_HOLD', _('On Hold')
    
    # Spaces can only be assigned to a User with the specific 'RENTER' role.
    renter = models.ForeignKey(
        CustomUser, 
        on_delete = models.CASCADE, 
        limit_choices_to = {'role': 'RENTER'}
    )
    
    # Location of the space
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    
    # Environment Conditions of the space
    environment_conditions = models.CharField(max_length = 8, choices = EnvironmentConditions.choices)
    
    # Height of the space
    height = models.IntegerField(default = SHELF_HEIGHT)

    # Status of the space
    status = models.CharField(max_length = 8, choices = Status.choices, default = Status.PENDING)

    # Price per day for a single shelf in the space
    price_per_day = models.DecimalField(max_digits = 4, decimal_places = 2, default = 1.00)

    # Description for the space
    description = models.TextField()

    @property
    def length(self):
        """
        Returns the length of the space based on its first rack.

        Returns:
            int: Length in cm.
        """
        return self.rack_set.first().length
    
    @property
    def width(self):
        """
        Returns the width of the space based on its first rack.

        Returns:
            int: Width in cm.
        """
        return self.rack_set.first().width
    
    @property
    def total_shelves(self):
        """
        Calculates the maximum number of standard shelves that fit in this space.

        Returns:
            int: Maximum shelf capacity.
        """
        return self.length * self.height // (self.rack_set.first().shelf_set.first().length * self.rack_set.first().shelf_set.first().height)
    
    @staticmethod
    def get_price(location: Location):
        """
        Returns the base price for a given Location.

        Args:
            location (Location): The location to query.

        Returns:
            Decimal: Daily price.
        """
        return location.price_per_day


class Rack(models.Model):
    """
    Represents a vertical shelving unit within a Space.
    """
    # Space that the rack belongs to
    space = models.ForeignKey(Space, on_delete = models.CASCADE)

    # Length of the rack
    length = models.IntegerField(default = SHELF_LENGTH)
    
    @property
    def width(self):
        """
        Returns the width of the Rack, which is a fixed constant SHELF_WIDTH.

        Returns:
            int: The fixed width defined in constants.
        """
        return self.shelf_set.first().width
    
    @property
    def height(self):
        """
        Returns the height of the Rack, which is a fixed constant SHELF_HEIGHT.

        Returns:
            int: The fixed height defined in constants.
        """
        return self.shelf_set.first().height


class Shelf(models.Model):
    """
    Represents a single rentable unit within a Rack.
    """
    # Rack that the shelf belongs to
    rack = models.ForeignKey(Rack, on_delete = models.CASCADE)

    # Unique Identifier for the shelf
    shelf_label = models.CharField(max_length = 3)
    
    # Flag for: Is the shelf currently not booked?
    is_available = models.BooleanField(default = True)

    @property
    def length(self):
        """
        Returns the fixed length of the Shelf unit.

        Returns:
            int: The fixed length defined in constants.
        """
        return SHELF_LENGTH
    
    @property
    def width(self):
        """
        Returns the fixed width of the Shelf unit.

        Returns:
            int: The fixed width defined in constants.
        """
        return SHELF_WIDTH
    
    @property
    def height(self):
        """
        Returns the fixed height of the Shelf unit.

        Returns:
            int: The fixed height defined in constants.
        """
        return SHELF_HEIGHT
