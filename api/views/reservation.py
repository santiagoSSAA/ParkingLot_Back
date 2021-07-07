""" Contains Reservation endpoint definition """

from cerberus import Validator
from datetime import datetime

from django.db.models import Q
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..helpers.token import TokenHandler
from ..helpers.paginator import paginate_content

from ..models.user import User
from ..models.parking_slot import ParkingSlot
from ..models.reservation import Reservation

from ..serializers.reservation import ReservationSerializer, ReservationClientSerializer


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
        payload, user = self.get_payload(request)
        def to_date(s): return datetime.strptime(s, '%Y-%m-%d %H:%M')
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        now = datetime.now()

        if user.profile == "user":
            validator = Validator({
                "initial_hour": {"required": False, "type": "datetime",
                    "coerce": to_date},
                "final_hour": {"required": False, "type": "datetime",
                    "coerce": to_date},
                "slot": {"required": False, "type": "string", "regex": r"\d+"},
                "number_plate": {"required": False, "type": "string"},
                "vehicle_type": {"required": False, "type": "string",
                    "allowed": ["auto","moto"] },
            })
        else:
            validator = Validator({
                "document": {"required": True, "type": "string"},
                "email": {"required": True, "type": "string"},
                "slot": {"required": False, "type": "string", "regex": r"\d+"},
                "initial_hour": {"required": True, "type": "datetime",
                    "coerce": to_date},
                "final_hour": {"required": False, "type": "datetime",
                    "coerce": to_date},
                "number_plate": {"required": True, "type": "string"},
                "vehicle_type": {"required": True, "type": "string",
                    "allowed": ["auto","moto"] },
            })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "cuerpo inválido",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data["vehicle_plate"] = request.data.pop("number_plate")
        if user.profile == "user":
            request.data["user"] = user

        if request.data.get("slot"):
            slot = ParkingSlot.objects.filter(pk=int(request.data.get("slot"))).first()
            if not slot:
                return Response({
                    "code": "slot_not_found",
                    "detailed": "Aparcamiento no encontrado"
                },status=status.HTTP_404_NOT_FOUND)

            if slot.get_status() != "Disponible":
                return Response({
                    "code": "slot_not_available",
                    "detailed": "Aparcamiento ocupado"
                },status=status.HTTP_409_CONFLICT)
            request.data["slot"] = slot
        else:
            slots = ParkingSlot.objects.filter(is_active=True)  
            slot_pks = [slot.pk for slot in slots if slot.get_status() == "Disponible"]
            slot = slots.filter(pk__in=slot_pks).order_by('-place_code').first()
            if not slot:
                return Response({
                    "code": "slots_fullfied",
                    "detailed": "Aparcamiento lleno"
                },status=status.HTTP_404_NOT_FOUND)
            request.data["slot"] = slot
        
        if request.data.get("initial_hour"):
             if (datetime.strptime(request.data.get("initial_hour"), '%Y-%m-%d %H:%M') < now):
                return Response({
                    "code": "invalid_initial_hour",
                    "detailed": "No se puede iniciar reservas con horas pasadas."
                },status=status.HTTP_409_CONFLICT)

        if not "initial_hour" in request.data:
            request.data["initial_hour"] = now.strftime('%Y-%m-%d %H:%M')

        if Reservation.objects.filter(
            Q(initial_hour=request.data.get("initial_hour")) |
            Q(final_hour=request.data.get("final_hour")), is_cancelled=False):
            return Response({
                "code": "invalid_range",
                "detailed": "Ya existe una reserva con la hora estipulada."
            },status=status.HTTP_409_CONFLICT)

        if (request.data.get("final_hour") and
            (datetime.strptime(request.data.get("final_hour"), '%Y-%m-%d %H:%M') - datetime.strptime(
                request.data.get("initial_hour"), '%Y-%m-%d %H:%M')).seconds / 3600 < 1):
            return Response({
                "code": "invalid_final_hour",
                "detailed": "La reservación debe durar al menos una (1) hora."
            },status=status.HTTP_409_CONFLICT)

        if "document" in request.data:
            request.data["document_number"] = request.data.pop("document")

        reservation = Reservation.objects.create(**request.data)
        return Response({"id": reservation.pk}, status=status.HTTP_201_CREATED)

    @paginate_content()
    def get(self, request):
        """ Retrieve a reservation list.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        payload, user = self.get_payload(request)
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        query = {}
        if user.profile != "admin":
            query["is_cancelled"] = False
            query["user"] = user
        if "user" in request.GET:
            query["user__document__icontains"] = request.GET["user"]
        if "slot" in request.GET:
            query["slot__place_code__icontains"] = request.GET["slot"]
        if "document_number" in request.GET:
            query["document_number__icontains"] = request.GET["document_number"]
        if "email" in request.GET:
            query["email__icontains"] = request.GET["email"]
        if "number_plate" in request.GET:
            query["vehiche_plate__icontains"] = request.GET["vehicle_plate"]
        if "vehicle_type" in request.GET:
            query["vehicle_type"] = request.GET["vehicle_type"]

        if query:
            data = Reservation.objects.filter(**query).order_by('-created')
        else:
            data = Reservation.objects.all().order_by('-created')

        if "status" in request.GET:
            reserve_pks = [reserve.pk for reserve in data if
            reserve.get_status() == request.GET["status"]]
            data = data.filter(pk__in=reserve_pks)
        if user.profile != "admin":
            reserve_pks = [reserve.pk for reserve in data if
            reserve.get_status() != "Finalizado"]
            data = data.filter(pk__in=reserve_pks)

        return Response({
            "code": data.count(),
            "data": (ReservationSerializer(data,many=True).data
            if user.profile == "admin" else ReservationClientSerializer(data,many=True).data)
        }, status=status.HTTP_200_OK)

class SpecificReservationApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to specific reservation model management. """
    def patch(self, request, *args, **kwargs):
        """ Update a reservation.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        payload, user = self.get_payload(request)
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        def to_date(s): return datetime.strptime(s, '%Y-%m-%d %H:%M')
        if user.profile == "admin":
            validator = Validator({
                "document": {"required": False, "type": "string"},
                "email": {"required": False, "type": "string"},
                "initial_hour": {"required": False, "type": "datetime",
                    "coerce": to_date},
                "final_hour": {"required": False, "type": "datetime",
                    "coerce": to_date},
                "slot": {"required": False, "type": "string", "regex": r"\d+"},
                "number_plate": {"required": False, "type": "string"},
                "vehicle_type": {"required": False, "type": "string",
                    "allowed": ["auto","moto"] }
            })
        else:
            validator = Validator({
                "initial_hour": {"required": False, "type": "datetime",
                    "coerce": to_date},
                "final_hour": {"required": False, "type": "datetime",
                    "coerce": to_date}
            })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "Cuerpo inválido",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if "number_plate" in request.data:
            request.data["vehicle_plate"] = request.data.pop("number_plate")

        if "document" in request.data:
            request.data["document_number"] = request.data.pop("document")

        if request.data.get("slot"):
            slot = ParkingSlot.objects.filter(pk=int(request.data.get("slot"))).first()
            if not slot:
                return Response({
                    "code": "slot_not_found",
                    "detailed": "Aparcamiento no encontrado"
                },status=status.HTTP_404_NOT_FOUND)

            if slot.get_status() != "Disponible":
                return Response({
                    "code": "slot_not_available",
                    "detailed": "Aparcamiento ocupado"
                },status=status.HTTP_409_CONFLICT)
            request.data["slot"] = slot

        reservation = Reservation.objects.filter(pk=kwargs["id"]).first()
        if not reservation:
            return Response({
                "code": "reservation_not_found",
                "detailed": "Reservación no encontrada"
            },status=status.HTTP_404_NOT_FOUND)

        if request.data.get("final_hour") and (
            datetime.now() - reservation.final_hour).seconds / 3600 < 1:
            return Response({
                "code": "cannot_extend",
                "detailed": "no se puede extender reservación"
            },status=status.HTTP_409_CONFLICT)

        Reservation.objects.filter(pk=kwargs["id"]).update(**request.data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ Retrieve a reservation.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        payload, user = self.get_payload(request)
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        reservation = Reservation.objects.filter(pk=kwargs["id"]).first()
        if not reservation:
            return Response({
                "code": "reservation_not_found",
                "detailed": "Reservación no encontrada"
            },status=status.HTTP_404_NOT_FOUND)

        if (reservation.initial_hour.replace(tzinfo=None) - datetime.now().replace(tzinfo=None)).seconds / 3600 < 1:
            return Response({
               "code": "timelapse_expired",
               "detailed": "tiempo disponible de campo expirado" 
            },status=status.HTTP_409_CONFLICT)

        if reservation.get_status()  == "Finalizado":
            return Response({
                "code": "not_valid_cancelation",
                "detailed": "No se puede cancelar reserva finalizada"
            },status=status.HTTP_409_CONFLICT)

        reservation.is_cancelled = True
        reservation.save()
        return Response(status=status.HTTP_200_OK)

class SpecificCostReservationApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to cost reservation model management. """
    def get(self, request, *args, **kwargs):
        """ retrieve payment price.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        payload, user = self.get_payload(request)
        if not payload:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.profile != "admin":
            return Response(status=status.HTTP_403_FORBIDDEN)

        reservation = Reservation.objects.filter(pk=kwargs["id"]).first()
        if not reservation:
            return Response({
                "code": "reservation_not_found",
                "detailed": "Reserva no encontrada"
            },status=status.HTTP_404_NOT_FOUND)

        if not reservation.user:
            final_hour = datetime.now()        
        else:
            final_hour = reservation.final_hour
        initial_hour = reservation.initial_hour

        type = reservation.vehicle_type
        if not final_hour or not initial_hour:
            return Response({
                "code": "hour_cannot_be_none",
                "detailed": "reservación con datos de horas vacías"
            }, status=status.HTTP_409_CONFLICT)

        hour = (final_hour - initial_hour).seconds // 3600
        return Response({"price": {"auto":settings.CAR_PRICE,"moto":settings.MOTO_PRICE}[type], "hours": hour}, status=status.HTTP_200_OK)