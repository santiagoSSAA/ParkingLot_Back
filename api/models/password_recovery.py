""" Contains the password recovery model """

from django.db import models
from django_extensions.db.models import TimeStampedModel

class PasswordRecovert(TimeStampedModel):
    """
    Extends class TimeStampedModel.
    This class add fields created and modified
    """
    user = models.ForeignKey("User", null=True, blank=True,
        on_delete=models.CASCADE, related_name="PR_user")
    expiration_date = models.DateTimeField("Fecha de vencimiento")
    is_used = models.BooleanField("Fue usado", default=False)
    token = models.TextField("Token")

    class Meta: # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Recuperación de contraseña"
        verbose_name_plural = "Recuperación de contraseña"

    def __str__(self):
        date = self.created.strftime("%Y-%m-%d")
        return f"{self.pk}. {date} | {self.user.email}"