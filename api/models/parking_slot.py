""" Contains the Parking slot model """

from django.db import models
from django_extensions.db.models import TimeStampedModel

from .reservation import Reservation

_SLOT_STATUS_CHOICES = (
    ("available","Disponible"),
    ("occupied","Ocupado"),
)

class ParkingSlot(TimeStampedModel):
    """
    Extends class TimeStampedModel.
    This class add fields created and modified
    """
    place_code = models.TextField("Código de aparcamiento", unique=True)
    status = models.CharField("Estado del aparcamiento",
        choices=_SLOT_STATUS_CHOICES, default="available")

    class Meta: #pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Aparcamiento"
        verbose_name_plural = "Lista de aparcamientos"

    def __str__(self):
        return f"{self.pk}. {self.place_code} - {self.status}"