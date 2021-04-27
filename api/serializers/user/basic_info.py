""" Contains User serializer definition """

import copy
from django.contrib.auth import get_user_model
from rest_framework import serializers


USER = get_user_model()


class BasicUserDisplaySerializer(serializers.ModelSerializer):
    """ Defines user serializer behaviour. """
    class Meta:  # pylint: disable=too-few-public-methods
        """ Defines serializer fields that are being used """

        model = USER
        fields = [
            'id', 'email', 'first_name', 'second_name',
            'last_name', 'cellphone', 'document',
            'creation_date'
        ]
