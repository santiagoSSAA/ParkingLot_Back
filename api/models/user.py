""" Contains the User model """

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import tree
from .profile import Profile


class User(AbstractUser):
    """
    Extends native django user model adding new features to user definition.
    """

    GENDER_CHOICES = (
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("U", "No definido"))

    birthdate = models.DateField("Fecha de nacimiento", blank=True, null=True)
    document = models.CharField("Documento", max_length=255, unique=True)
    name = models.CharField("Primer Nombre", max_length=255)
    cellphone = models.CharField("Celular", max_length=11, blank=True)
    state = models.CharField("Departamento", max_length=100, blank=True)
    city = models.CharField("Ciudad", max_length=100, blank=True)
    address = models.CharField("Direccion", max_length=100, blank=True)
    gender = models.CharField(
        "Género", max_length=1, choices=GENDER_CHOICES, blank=True)
    profile = models.ManyToManyField(Profile, related_name='user_profile')
    number_plate = models.CharField(
        "Numero de placa del vehiculo", max_length=6)

    REQUIRED_FIELDS = ['email']

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return '{} - {} {}'.format(self.pk, self.document, self.email)
