"""
Database models for tracking rental transactions.
"""
from django.db import models
from users.models import CustomUser
from listings.models import Rack
from django.utils.translation import gettext_lazy as _

class Booking(models.Model):
    """
    Represents a booking of specific shelves within a Rack.

    Links a Lessee to a Rack for a specific duration.
    """
    class Status(models.TextChoices):
        BOOKED = 'BOOKED', _('Booked')
        ACTIVE = 'ACTIVE', _('Active')
        PAST = 'PAST', _('Past')
        CANCELLED = 'CANCELLED', _('Cancelled')
    

    lessee = models.ForeignKey(CustomUser, on_delete = models.CASCADE, limit_choices_to = {'role': CustomUser.Roles.LESSEE})
    
    rack = models.ForeignKey(Rack, on_delete = models.CASCADE)

    num_shelves_occupied = models.IntegerField(default = 1)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    total_price = models.DecimalField(max_digits = 6, decimal_places = 2)
    
    status = models.CharField(max_length = 10, choices = Status.choices, default = Status.BOOKED)

    occupying_space = models.BooleanField(default = False)
