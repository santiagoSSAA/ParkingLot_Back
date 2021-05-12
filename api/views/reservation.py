""" Contains Reservation endpoint definition """

from cerberus import Validator

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...helpers.token import TokenHandler
from ...helpers.paginator import paginate_content

from ..models.user import User
from ..models.parking_slot import ParkingSlot


class ReservationApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to reservation model management. """

    def post(self, request):
        """ Create a reservation.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        def to_date(s): return datetime.strptime(s, '%Y-%m-%d %H:%M')
        validator = Validator({
            "document": {"required": False, "type": "string"},
            "email": {"required": False, "type": "string"},
            "initial_hour": {"required": True, "type": "datetime",
                "coerce": to_date},
            "final_hour": {"required": False, "type": "datetime",
                "coerce": to_date},
            "slot": {"required": True, "type": "integer"},
            "user": {"required": False, "type": "integer"},
            "vehicle_plate": {"required": True, "type": "string"},
            "vehicle_type": {"required": True, "type": "string",
                "allowed": ["auto","moto"] },
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if ("user" not in request.data and all(
            elem in ["document", "email"] for elem in request.data.keys())):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
                "data": "Se debe ingresar document y email en caso de no ingresar user"
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get("user") and not User.objects.filter(
            pk=request.data.get("user")):
            return Response({
                "code": "user_not_found",
                "detailed": "Usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        if request.data.get("user"):
            request.data["user"] = User.objects.filter(
                pk=request.data.get("user")).first()

        if not ParkingSlot.objects.filter(pk=request.data.get("slot")):
            return Response({
                "code": "slot_not_found",
                "detailed": "Aparcamiento no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        request.data["slot"] = ParkingSlot.objects.filter(
            pk=request.data.get("slot")).first()
        
        if (request.data.get("final_hour") and
            (request.data.get("final_hour") - request.data.get("initial_hour")).seconds / 3600 < 1):
            return Response({
                "code": "invalid_final_hour",
                "detailed": "La reservación debe durar al menos una (1) hora."
            },status=status.HTTP_409_CONFLICT)

        reservation = reservation.objects.create(**request.data)
        return Response({"id": reservation.pk}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """ Create a reservation.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """