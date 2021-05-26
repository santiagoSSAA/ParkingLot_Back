""" Contains Payment endpoint definition """
from cerberus import Validator

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..helpers.token import TokenHandler
from ..helpers.paginator import paginate_content

from ..models.payment import Payment, _PAYMENT_STATUS_CHOICES
from ..models.reservation import Reservation

from ..serializers.payment import PaymentSerializer


class PaymentApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to payment model management. """
    def post(self, request):
        """ Create a payment.

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

        validator = Validator({
            "reservation": {"required": True, "type": "integer"},
            "price": {"required": True, "type": "integer"},
            "concept": {"required": True, "type": "string"},
            "status": {"required": True, "type": "string", "allowed": [
                e[1] for e in _PAYMENT_STATUS_CHOICES]},
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        reservation = Reservation.objects.filter(pk=request.data.get("reservation")).first()
        if not reservation:
            return Response({
                "code": "resrvation_not_found",
                "detailed": "Reservación no encontrada"
            },status=status.HTTP_404_NOT_FOUND)
        request.data["reservation"] = reservation

        if Payment.objects.filter(reservation=reservation, status="approved"):
            return Response({
                "code": "resrvation_already_payed",
                "detailed": "Reservación ya paga"
            },status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(**request.data)
        return Response({"created": payment.pk}, status=status.HTTP_201_CREATED)

    def get(self, request):
        """ retrieve a payment, but in plural lmao.

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
        
        query = {}
        if "id" in request.GET:
            query["pk"] = request.GET["id"]
        if "reservation" in request.GET:
            reservation = Reservation.objects.filter(pk=request.data.get("reservation")).first()
            if not reservation:
                return Response({
                    "code": "reservation_not_found",
                    "detailed": "Reservación no encontrada"
                },status=status.HTTP_404_NOT_FOUND)
            query["reservation"] = reservation
        if "status" in request.GET:
            query["status"] = request.GET["status"]

        if query:
            count = Payment.object.filter(**query).count()
            payments = Payment.object.filter(**query)
        else:
            count = Payment.object.all().count()
            payments = Payment.object.all()

        return Response({
            "count": count,
            "data": PaymentSerializer(payments,many=True).data
        },status=status.HTTP_200_OK)