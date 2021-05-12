""" Contains User endpoint definition """
from cerberus import Validator
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...helpers.token import TokenHandler
from ...helpers.paginator import paginate_content

from ...models.user import User

from ...serializers.user import UserSerializer


class UserApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to user model management. """

    def post(self, request):
        """ Create an user.

        Parameters
        ----------

        request (dict)
            Contains http transaction information.

        Returns
        -------
            Response (JSON, int)
                Body response and status code.

        """
        def to_date(s): return datetime.strptime(s, '%Y-%m-%d')
        validator = Validator({
            "birthdate": {"required": True, "type": "date", "coerce": to_date},
            "document": {"required": True, "type": "string"},
            "name": {"required": True, "type": "string"},
            "email": {"required": True, "type": "string"},
            "password": {"required": True, "type": "string", "minlength": 7},
            "cellphone": {"required": True, "type": "string"},
            "gender": {
                "required": True, "type": "string", "allowed": ["M", "F", "U"]},
            "number_plate": {"required": True, "type": "string"},
            "vehicle_type": {"required": False, "type": "string",
                "allowed": ["auto","moto"] }
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "cuerpo inválido",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'code': 'invalid_body',
                'detailed': 'Cuerpo de la petición con estructura inválida',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(
            Q(email=request.data['email']) |
            Q(document=request.data['document'])
        ).first()

        if user:
            return Response({
                "code": "user_already_exist",
                "detailed": "El usuario ya existe en la base de datos"
            }, status=status.HTTP_409_CONFLICT)

        user = serializer.create(request.data)

        return Response({
            "inserted": user.pk,
        }, status=status.HTTP_201_CREATED)

    @paginate_content()
    def get(self, request):
        """ Retrieve user list.

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

        validator = Validator({
            "document": {"required": False},
            "email": {"required": False},
            "name": {"required": False},
        })
        if not validator.validate(request.GET):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        query = {}

        if 'document' in request.GET:
            query['document__icontains'] = request.GET['document']
        if 'email' in request.GET:
            query['email__icontains'] = request.GET['email']
        if 'name' in request.GET:
            query['name__icontains'] = request.GET['name']

        if query:
            count = User.objects.filter(**query).count()
            users = User.objects.filter(**query).order_by('-creation_date')[
                self.pagination_start: self.pagination_end + 1]
        else:
            count = User.objects.all().count()
            users = User.objects.all().order_by('-creation_date')[
                self.pagination_start: self.pagination_end + 1]

        return Response({
            'count': count,
            'data': UserSerializer(users, many=True).data,
        }, status=status.HTTP_200_OK)

class SpecificUserApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to specific user model management. """

    def get(self, request, *args, **kwargs):
        """ Retrieve user list.

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

        consulted_user = User.objects.filter(pk=kwargs["id"]).first()
        if not consulted_user:
            return Response({
                "code": "user_not_found",
                "detailed": "usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        if user.profile != "admin" and user != consulted_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response({
            'data': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """ Update user information.

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
            "document": {"required": False, "type": "string"},
            "name": {"required": False, "type": "string"},
            "cellphone": {"required": False, "type": "string"},
            "gender": {
                "required": False, "type": "string", "allowed": ["M", "F", "U"]},
            "number_plate": {"required": False, "type": "string"},
            "vehicle_type": {"required": False, "type": "string",
                "allowed": ["auto","moto"] }
        })
        if not validator.validate(request.data):
            return Response({
                "code": "invalid_body",
                "detailed": "cuerpo inválido",
                "data": validator.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        consulted_user = User.objects.filter(pk=kwargs["id"]).first()
        if not consulted_user:
            return Response({
                "code": "user_not_found",
                "detailed": "usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        if user.profile != "admin" and user != consulted_user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if (request.data.get("document") and User.objects.filter(
            document=request.data.get("document")).exclude(pk=kwargs["id"])):
            return Response({
                "code": "document_already_in_use",
                "detailed": "Documento ya registrado"
            },status=status.HTTP_409_CONFLICT)

        if (request.data.get("number_plate") and User.objects.filter(
            document=request.data.get("number_plate")).exclude(pk=kwargs["id"])):
            return Response({
                "code": "number_plate_already_in_use",
                "detailed": "Placa ya registrado"
            },status=status.HTTP_409_CONFLICT)

        User.objects.filter(pk=kwargs["id"]).update(**request.data)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ delete user.

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

        deleted_user = User.objects.filter(pk=kwargs["id"]).first()
        if not deleted_user:
            return Response({
                "code": "user_not_found",
                "detailed": "usuario no encontrado"
            },status=status.HTTP_404_NOT_FOUND)

        deleted_user.is_active = False
        deleted_user.save()
        return Response(status=status.HTTP_200_OK)