""" Contains the User model """

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extends native django user model adding new features to user definition.
    """

    GENDER_CHOICES = (
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("U", "No definido"))

    VEHICLE_TYPE = (
        ("auto", "Automovil"),
        ("moto", "Motocicleta"),
    )

    PROFILE_CHOICES = (
        ("user", "Cliente"),
        ("admin", "Administrador")
    )

    birthdate = models.DateField("Fecha de nacimiento", blank=True, null=True)
    document = models.CharField("Documento", max_length=255, unique=True)
    name = models.CharField("Nombres", max_length=255)
    cellphone = models.CharField("Celular", max_length=11, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.EmailField("Correo", unique=True)
    gender = models.CharField(
        "Género", max_length=1, choices=GENDER_CHOICES, blank=True)
    profile = models.CharField("Perfil", max_length=255, choices=PROFILE_CHOICES, 
        default="user")
    number_plate = models.CharField(
        "Numero de placa del vehiculo", max_length=6, null=True, blank=True)
    vehicle_type = models.TextField("Tipo de vehículo", choices=VEHICLE_TYPE,
        null= True, blank=True)

    REQUIRED_FIELDS = ['email']

    class Meta:  # pylint: disable=too-few-public-methods
        """ Sets human readable name """
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return '{} - {} {}'.format(self.pk, self.document, self.email)
