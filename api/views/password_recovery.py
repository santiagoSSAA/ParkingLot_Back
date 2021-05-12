""" Contains Password Recovery endpoint definition """
from cerberus import Validator
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..helpers.email import send_email
from ..helpers.token import TokenHandler
from ..helpers.paginator import paginate_content

from ..models.password_recovery import PasswordRecovery
from ..models.user import User

_EMAIL_MESSAGE = (
    'Hola, {}.<br><br>Para poder continuar el proceso de '
    'recuperación de tu contraseña. Por favor, entra al siguiente <a '
    'href="{}">enlace</a>')


class PasswordRecoveryApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to password recovery model management. """

    def post(self, request):
        """ Creates a token for password recovery.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        validator = Validator({
            "email": {
                "required": True,
                "type": "string",
                "regex": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            },
            "type": {"required": True, "type": "string", "allowed": ["Usuario", "Empresa","Inmobiliaria"]}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "Cuerpo con estructura inválida",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        request.data["email"] = request.data["email"].lower()
        
        user = User.objects.filter(email=request.data["email"]).first()
        if not user:
            return Response({
                "code": "user_not_found",
                "detailed": "usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        token = get_random_string(70)
        data = {
            "expiration_date": (datetime.now() + timedelta(minutes=15)),
            "is_user": False,
            "token": token,
            "user": user
        }
        PasswordRecovery.objects.create(**data)
        send_email("Recuperación de contraseña", _EMAIL_MESSAGE.format(
            user.first_name,
            f"{settings.HOSTNAME}/recuperar-contraseña/{token}"),
            request.data["email"])
        return Response(status=status.HTTP_201_CREATED)

class SpecificPasswordRecoveryApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to specific password recovery model management. """

    def patch(self, request, *args, **kwargs):
        """ update a token for password recovery.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        validator = Validator({
            "new": {"required": True, "type": "string",
            "regex":r'^.*(?=.{8,100})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9]+$'}
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "Cuerpo con estructura inválida",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        recover_request = PasswordRecovery.objects.filter(
            token=kwargs["token"]).first()
        if not recover_request:
            return Response({
                "code": "token_not_found",
                "detailed": "Token no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)
        if (recover_request.is_used or
                dt.datetime.now() >= recover_request.expiration_date.replace(
                    tzinfo=None)):
            PasswordRecovery.objects.filter(
                token=kwargs["token"]).delete()
            return Response({
                "code": "token_expired_or_used",
                "detailed": "Token ya usado o vencido"
            }, status=status.HTTP_409_CONFLICT)

        User.objects.filter(email=recover_request.email).update(
            password=make_password(request.data["new"]))
        return Response(status=status.HTTP_200_OK)