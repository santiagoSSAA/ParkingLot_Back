""" Contains the Profile model """

from rest_framework import serializers
from ...models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """ Defines profile serializer behaviour. """

    class Meta:  # pylint: disable=too-few-public-methods
        """ Defines serializer fields that are being used """

        model = Profile
        fields = ['names']
