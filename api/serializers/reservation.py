""" Contains Reservation serializer definition """
from rest_framework import serializers

from ..models.reservation import Reservation

from ..serializers.user.basic_info import BasicUserDisplaySerializer

class ReservationSerializer(serializers.ModelSerializer):
    """ Defines Reservation serializer behaviour. """
    user = BasicUserDisplaySerializer()

    class Meta: # pylint: disable=too-few-public-methods        
        model = Reservation
        fields = ["user", "initial_hour", "final_hour", "vehicle_plate",
        "vehicle_type", "slot", "document_number", "email", "is_cancelled"]