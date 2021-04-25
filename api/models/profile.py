""" Contains the Profile model"""

from django.db import models


class Profile(models.Model):
    """ Profile model """

    names = models.CharField("Nombres de los perfiles", max_length=255)

    class Meta:
        """ Sets human readable name """
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return self.names
