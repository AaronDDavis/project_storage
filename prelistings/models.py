"""
Models for the pre-approval workflow (Installation Requests).
"""
from django.db import models
from listings.models import EnvironmentConditions, Location
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class InstallationRequest(models.Model):
    """
    Represents a request by a Renter to install shelves at a location.

    Once 'COMPLETED', this object is converted into a live Space.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        COMPLETED = 'COMPLETED', _('Completed')

    renter = models.ForeignKey(CustomUser, on_delete = models.CASCADE, limit_choices_to = {'role': CustomUser.Roles.RENTER})
    
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    environment_conditions = models.CharField(max_length = 8, choices = EnvironmentConditions.choices)

    status = models.CharField(max_length = 10, choices = Status.choices, default = Status.PENDING)

    price_per_day = models.DecimalField(max_digits = 4, decimal_places = 2, default = 1.00)
    description = models.TextField()

    num_rack = models.IntegerField(default = 0, editable = True)
    num_shelves_per_rack = models.IntegerField(default = 0, editable = True)
