""" Contains Reservation serializer definition """
from rest_framework import serializers

from ..models.reservation import Reservation

from ..serializers.user.basic_info import BasicUserDisplaySerializer

class ReservationClientSerializer(serializers.ModelSerializer):
    """ Defines Reservation serializer behaviour. """
    status = serializers.CharField(source="get_status")
    number_plate = serializers.SerializerMethodField("get_plate")
    slot = serializers.SerializerMethodField("get_slot")
    class Meta: # pylint: disable=too-few-public-methods        
        model = Reservation
        fields = ["id", "initial_hour", "final_hour", "number_plate",
        "vehicle_type", "slot", "status"]

    def get_slot(self, obj):
        return obj.slot.place_code

    def get_plate(self, obj):
        return obj.vehicle_plate

class ReservationSerializer(serializers.ModelSerializer):
    """ Defines Reservation serializer behaviour. """
    user = BasicUserDisplaySerializer()
    number_plate = serializers.SerializerMethodField("get_plate")
    status = serializers.CharField(source="get_status")

    class Meta: # pylint: disable=too-few-public-methods        
        model = Reservation
        fields = ["id", "user", "initial_hour", "final_hour", "number_plate",
        "vehicle_type", "slot", "document_number", "email", "status", "is_cancelled"]

    def get_plate(self, obj):
        return obj.vehicle_plate