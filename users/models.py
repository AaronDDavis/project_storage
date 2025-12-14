"""
Extends the standard Django User model with NRIC and Role fields.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model with RBAC support.

    Attributes:
        role (str): 'RENTER' or 'LESSEE'.
        nric_fin (str): National identification number.
    """

    class Roles(models.TextChoices):
        RENTER = 'RENTER', _('Renter')
        LESSEE = 'LESSEE', _('Lessee')
    
    role = models.CharField(
        max_length=6, 
        choices=Roles.choices
    )
    
    nric_fin = models.CharField(
        max_length=9
    )

    @property
    def is_renter(self) -> bool:
        """
        Returns True if the user has the RENTER role.
        """
        return self.role == CustomUser.Roles.RENTER

    @property
    def is_lessee(self) -> bool:
        """
        Returns True if the user has the LESSEE role.
        """
        return self.role == CustomUser.Roles.LESSEE
