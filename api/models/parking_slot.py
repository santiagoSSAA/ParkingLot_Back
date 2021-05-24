""" Contains the Parking slot model """

from django.db import models
from django.db.models import Q
from django_extensions.db.models import TimeStampedModel

from .reservation import Reservation


class ParkingSlot(TimeStampedModel):
    """
    Extends class TimeStampedModel.
    This class add fields created and modified
    """
    place_code = models.TextField("Código de aparcamiento", unique=True)
    is_active = models.BooleanField("está activo", default=True)

    class Meta: #pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Aparcamiento"
        verbose_name_plural = "Lista de aparcamientos"

    def __str__(self):
        return f"{self.pk}. {self.place_code} - {self.status}"

    def get_status(self):
        if Reservation.objects.filter((Q(get_status="Vigente")|Q(get_status="Próximo")),
        slot=self):
            return "Ocupado"
        return "Disponible"
        
