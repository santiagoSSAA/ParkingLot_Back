""" Contains Reservation serializer definition """
from rest_framework import serializers

from ..models.reservation import Reservation

from ..serializers.user.basic_info import BasicUserDisplaySerializer

class ReservationClientSerializer(serializers.ModelSerializer):
    """ Defines Reservation serializer behaviour. """
    status = serializers.CharField(source="get_status")
    slot = serializers.SerializerMethodField("get_slot")
    class Meta: # pylint: disable=too-few-public-methods        
        model = Reservation
        fields = ["id", "initial_hour", "final_hour", "vehicle_plate",
        "vehicle_type", "slot", "status"]

    def get_slot(self, obj):
        return obj.slot.place_code

class ReservationSerializer(serializers.ModelSerializer):
    """ Defines Reservation serializer behaviour. """
    user = BasicUserDisplaySerializer()
    status = serializers.CharField(source="get_status")

    class Meta: # pylint: disable=too-few-public-methods        
        model = Reservation
        fields = ["id", "user", "initial_hour", "final_hour", "vehicle_plate",
        "vehicle_type", "slot", "document_number", "email", "status", "is_cancelled"]