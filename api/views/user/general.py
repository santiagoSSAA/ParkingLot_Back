""" Contains User endpoint definition """
from cerberus import Validator

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...helpers.token import TokenHandler
from ...helpers.paginator import paginate_content
from ...serializers.user import UserSerializer


class UserApi(APIView, TokenHandler):
    """ Defines the HTTP verbs to user model management. """

    def post(self, request):
        """ Retrieves all users instances.

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
            "address": {"required": True, "type": "string"},
            "state": {"required": True, "type": "string"},
            "city": {"required": True, "type": "string", "minlength": 2},
            "password": {"required": True, "type": "string", "minlength": 7},
            "cellphone": {"required": True, "type": "string"},
            "gender": {
                "required": True, "type": "string", "allowed": ["M", "F", "U"]},
            "number_plate": {"required": True, "type": "string"},
        })
        if not validator.validate(request.GET):
            return Response({
                "code": "invalid_filtering_params",
                "detailed": "Parámetros de búsqueda inválidos",
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
