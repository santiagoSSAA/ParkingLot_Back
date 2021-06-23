""" Contains Auth endpoint definition """

from cerberus import Validator
from datetime import timedelta
import jwt

from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.auth import Auth
from ..models.user import User


class AuthApi(APIView):
    """ Defines the HTTP verbs to auth model management. """

    def post(self, request):
        """ Creates a new session.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (int)
                Response status code.

        """
        validator = Validator({
            "user": {"required": True, "type": "string"},
            "password": {"required": True, "type": "string", "minlength": 7},
            "keep_logged_in": {"required": True, "type": "boolean"},
            "type": {"required": True, "type": "string", "allowed": ["user", "admin"]},
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "Cuerpo con estructura inválida",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=request.data["user"],
            profile=request.data["type"]).first()
        if not user:
            type = request.data["type"]
            return Response({
                "code": f"{type}_not_found",
                "detailed": "usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)       

        if not check_password(request.data["password"], user.password):
            return Response({
                "code": "incorrect_password",
                "detailed": "Contraseña incorrecta."
            },status=status.HTTP_401_UNAUTHORIZED)

        refresh = get_random_string(30)
        expiration = (settings.TOKEN_SHORT_EXP if not
            request.data["keep_logged_in"] else settings.TOKEN_LONG_EXP)
        token = jwt.encode({
            "expiration_date": str(datetime.now() + timedelta(hours=expiration)),
            "email": user.email,
            "type": request.data["type"],
            "refresh": refresh
        }, settings.SECRET_KEY, algorithm='HS256')

        Auth.objects.create(token=token)
        return Response({
            "id": user.pk,
            "token": token,
            "refresh": refresh,
            "profile": user.profile
        },status=status.HTTP_201_CREATED)

    def patch(self, request):
        """ Disables a session.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (int)
                Response status code.

        """
        header = request.headers.get("Authorization", None)

        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        session = Auth.objects.filter(token=header.split(" ")[1])
        if not session:
            return Response(status=status.HTTP_404_NOT_FOUND)

        session.update(is_disabled=True)
        return Response(status=status.HTTP_200_OK)

class RefreshTokenApi(APIView):
    """ Defines the HTTP verbs to refresh token. """

    def patch(self, request, *args, **kwargs):
        """ Refreshes a token.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (int)
                Response status code.

        """
        header = request.headers.get("Authorization", None)
        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            token = jwt.decode(header.split(" ")[1], settings.SECRET_KEY)
        except jwt.InvalidTokenError:
            return Response({
                "code": "invalid_token",
                "detailed": "Token inválido"
            }, status=status.HTTP_400_BAD_REQUEST)

        if token["refresh"] != kwargs["refresh"]:
            return Response(    {
                "code": "do_not_have_permission",
                "detailed": "No tienes permiso para ejecutar esta acción."
            }, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.filter(email=request.data["user"],
            profile=request.data["type"]).first()
        if not user:
            type = request.data["type"]
            return Response({
                "code": f"{type}_not_found"
            },status=status.HTTP_404_NOT_FOUND)
        
        refresh = get_random_string(30)
        expiration = (settings.TOKEN_SHORT_EXP if not
            request.data["keep_logged_in"] else settings.TOKEN_LONG_EXP)
        token = jwt.encode({
            "expiration_date": str(datetime.now() + timedelta(hours=expiration)),
            "email": user.email,
            "type": request.data["type"],
            "refresh": refresh
        }, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        session = Auth.objects.filter(token=header.split(" ")[1])
        if not session:
            return Response({
                "code": "token_not_found",
                "detailed": "Token no existe en la base de datos"
            }, status=status.HTTP_404_NOT_FOUND)

        session.update(token=token)
        Auth.objects.create(token=token)
        return Response({
            "id": user.pk,
            "token": token,
            "refresh": refresh,
            "profile": user.profile
        },status=status.HTTP_201_CREATED)