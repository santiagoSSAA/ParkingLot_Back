""" Contains the Payment model """

from django.db import models
from django_extensions.db.models import TimeStampedModel

_PAYMENT_STATUS_CHOICES = (
    ("approved", "Aprobado"),
    ("rejected", "Rechazado"),
    ("pending", "Pendiente"),
    ("failed", "Fallida"),
    ("abandoned", "Abandonada"),
    ("cancelled", "Cancelado")
)

class Payment(TimeStampedModel):
    """
    Extends class TimeStampedModel.
    This class add fields created and modified
    """
    reservation = models.ForeignKey("Reservation", null=True, blank=True)
    price = models.IntegerField("Valor", default=0)
    concept = models.TextField("concepto", default="")
    status = models.CharField("Estado", max_length=25,
        choices=_PAYMENT_STATUS_CHOICES, default="pending")

    class Meta: # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        date = self.created.strftime("%Y-%m-%d")
        return f"{self.pk}. {date} | {self.status} - {self.concept}"