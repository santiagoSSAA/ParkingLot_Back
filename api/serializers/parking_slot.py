""" Contains Parking slot serializer definition """
from django.db.models import Q
from rest_framework import serializers

from ..models.parking_slot import ParkingSlot
from ..models.reservation import Reservation
from ..models.user import User

from ..serializers.reservation import ReservationSerializer


class ParkingSlotClientSerializer(serializers.ModelSerializer):
    """ Defines Parking slot serializer behaviour. """
    status = serializers.CharField(source="get_status")

    class Meta: # pylint: disable=too-few-public-methods
        model = ParkingSlot
        fields = ["id", "place_code", "status"]

class ParkingSlotSerializer(serializers.ModelSerializer):
    """ Defines Parking slot serializer behaviour. """
    reservation = serializers.SerializerMethodField("get_reservation")
    reservation = serializers.serialize('json', self.get_reservation())
    status = serializers.CharField(source="get_status")

    class Meta: # pylint: disable=too-few-public-methods
        model = ParkingSlot
        fields = ["id", "place_code", "reservation", "status"]

    def get_reservation(self,obj):
        reservations = Reservation.objects.filter(slot=obj)
        reserve_pk = [rese.pk for rese in reservations if rese.get_status() in ["Vigente", "Próximo"]]
        reservation = reservations.filter(pk__in=reserve_pk).first()
        return None if not reservation else ReservationSerializer(reservation).data