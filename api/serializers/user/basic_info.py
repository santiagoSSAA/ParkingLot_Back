""" Contains User serializer definition """

import copy
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...models.user import User


class BasicUserDisplaySerializer(serializers.ModelSerializer):
    """ Defines user serializer behaviour. """
    class Meta:  # pylint: disable=too-few-public-methods
        """ Defines serializer fields that are being used """

        model = User
        fields = [
            'id', 'email', 'name', 'cellphone', 'document',
            'creation_date', 'birthdate', 'gender', 'profile',
            'number_plate', 'vehicle_type'
        ]
