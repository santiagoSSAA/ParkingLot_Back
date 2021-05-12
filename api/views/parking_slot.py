""" Contains Parking Slot endpoint definition """
from cerberus import Validator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...helpers.token import TokenHandler
from ...helpers.paginator import paginate_content

from ..models.parking_slot import ParkingSlot

from ..serializers.parking_slot import ParkingSlotSerializer
from ..serializers.parking_slot import ParkingSlotClientSerializer


class ParkingSlotApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to parking slot model management. """

    def post(self, request):
        """ Create a parking slot.

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
        if not payload or user.status == "pending":
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.profile != "admin":
            return Response(status=status.HTTP_403_FORBIDDEN)

        validator = Validator({"place_code": {"required": True,
        "type": "string"}})
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "cuerpo inválido",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if ParkingSlot.objects.filter(
            place_code=request.data.get("place_code"),is_active=True):
            return Repsonse({
                "code": "slot_already_exists",
                "code": "Estacionamiento ya registrado"
            },status=status.HTTP_409_CONFLICT)

        request.data["place_code"] = request.data["place_code"].upper()
        slot = ParkingSlot.objects.create(**request.data)
        return Response({"created": slot.pk}, status=status.HTTP_201_CREATED)

    @paginate_content()
    def get(self, request):
        """ Retrieve a list of slots.

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
        if not payload or user.status == "pending":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        validator = Validator({
            "place_code": {"required": False,"type": "string"},
            "status": {"required": False, "type": "string",
                "allowed": ["Ocupado", "Disponible"]}
        })
        if not validator.validate(request.GET):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        query = {}
        if request.GET.get("place_code"):
            query["place_code"] = request.GET.get("place_code")
        if user.profile == "client":
            query["is_active"] = True
        
        slots = ParkingSlot.objects.filter(**query)
        if slots and request.GET.get("status"):
            slots = [slot.id for slot in slots
                if slot.get_status() == request.GET.get("place_code")]
            slots = ParkingSlot.objects.filter(pk__in=slots)

        count = slots.count()
        data = slots.order_by('-creation_date')[
            self.pagination_start: self.pagination_end + 1]
        return Response({
            'count': count,
            'data': (ParkingSlotClientSerializer(data,many=True)
                if user.profile == "client" else ParkingSlotSerializer(data,many=True)
            ).data,
        }, status=status.HTTP_200_OK)


class SpecificParkingSlotApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to specific parking slot model management. """

    def get(self, request, *args, **kwargs):
        """ Retrieve specific slot information.

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
        if not payload or user.status == "pending":
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.profile != "admin":
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        slot = ParkingSlot.objects.filter(
            pk=kwargs["id"],is_active=True).first()
        if not slot:
            return Response({
                "code": "slot_not_found",
                "detailed": "aparcamiento no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        return Response({
            "data": ParkingSlotSerializer(slot).data
        },status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """ Update an slot information.

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
        if not payload or user.status == "pending":
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.profile != "admin":
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        validator = Validator({"place_code": {"required": False,"type": "string"}})
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "cuerpo inválido",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        if not ParkingSlot.objects.filter(pk=kwargs["id"],is_active=True):
            return Response({
                "code": "slot_not_found",
                "detailed": "aparcamiento no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        ParkingSlot.objects.filter(pk=kwargs["id"]).update(**request.data)
        return Reponse(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ Delete slot information.

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
        if not payload or user.status == "pending":
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if user.profile != "admin":
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        slot = ParkingSlot.objects.filter(
            pk=kwargs["id"],is_active=True).first()
        if not slot:
            return Response({
                "code": "slot_not_found",
                "detailed": "aparcamiento no encontrado"
            },status=status.HTTP_404_NOT_FOUND)
        slot.is_active = False
        slot.save()
        return Reponse(status=status.HTTP_200_OK)