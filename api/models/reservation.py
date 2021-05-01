""" Contains the reservation model """

from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

_VEHICLE_TYPE = (
    ("auto", "Automovil"),
    ("moto", "Motocicleta"),
)

class Reservation(TimeStampedModel):
    """
    Extends class TimeStampedModel.
    This class add fields created and modified
    """

    user = models.ForeignKey("User", null=True, blank=True,
        on_delete=models.CASCADE, related_name="reservation")
    initial_hour = models.DateTimeField("Hora de inicio")
    final_hour = models.DateTimeField("Hora de finalización", null=True,
        blank=True)
    vehicle_plate = models.TextField("Placa de vehículo")
    vehicle_type = models.TextField("Tipo de vehículo", choices=_VEHICLE_TYPE,
        default="auto")
    slot = models.ForeignKey("ParkingSlot", null=True, blank=True,
        on_delete=models.CASCADE, related_name="slot")
    document_number = models.TextField("Número de documento", null=True,
        blank=True)
    email = models.TextField("Correo electrónico", null=True, blank=True)
    is_cancelled = models.BooleanField("Cancelado", default=False)

    class Meta: # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Reserva"
        verbose_name_plural = "Reservaciones"

    def __str__(self):
        date = self.created.strftime("%Y-%m-%d")
        initial = self.initial_hour.strftime("%H:%M")
        final = self.final_hour.strftime("%H:%M") if self.final_hour else "ilimitado"
        return f"{self.pk}. ({date}) | {initial} - {final} | {self.get_status()}"

    def is_finished(self):
        if self.final_hour and self.final_hour < timezone.now():
            return True
        return False

    def is_current(self):
        if self.initial_hour <= timezone.now() and not self.is_finished():
            return True
        return True

    def get_status(self):
        # final_hour > now > initial_hour
        if self.is_cancelled or self.is_finished(): return "Finalizado"
        if self.is_current(): return "Vigente"
        return "Próximo"