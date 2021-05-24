""" Contains Payment endpoint definition """
from cerberus import Validator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..helpers.token import TokenHandler
from ..helpers.paginator import paginate_content

from ..models.payment import Payment, _PAYMENT_STATUS_CHOICES

class Payment(APIView, TokenHandler):
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

        pass

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
        pass