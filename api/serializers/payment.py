""" Contains Payment serializer definition """
from rest_framework import serializers

from ..models.payment import Payment

from .reservation import ReservationSerializer

class PaymentSerializer(serializers.ModelSerializer):
    """ Defines Payment serializer behaviour. """
    reservation = ReservationSerializer()

    class Meta: # pylint: disable=too-few-public-methods
        model = Payment
        fields = ["reservation", "price", "concept", "status"]