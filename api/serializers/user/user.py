""" Contains User serializer definition """
import copy
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .profile import ProfileSerializer
from ...services.user_register import UserProfiles


USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ Defines user serializer behaviour. """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=USER.objects.all())]
    )
    profile = ProfileSerializer(read_only=True, many=True, required=False)
    document = serializers.CharField(
        validators=[UniqueValidator(queryset=USER.objects.all())])

    class Meta:  # pylint: disable=too-few-public-methods
        """ Defines serializer fields that are being used """

        model = USER
        fields = [
            'id', 'email', 'name', 'birthdate', 'gender', 'cellphone',
            'state', 'city', 'address', 'document', 'profile',
            'creation_date', 'number_plate'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Creates an user object with its password and relate it with
            its profiles.

        Parameters:
            validated_data (dict):Contains the data from user that is going to
                                  be created.

        Returns:
            user (User): A fields-full custom django user.

        """

        aux = copy.deepcopy(validated_data)

        aux['username'] = aux['email'].lower()
        aux['email'] = aux['email'].lower()
        aux['password'] = make_password(validated_data['password'])

        user = USER.objects.create(**aux)
        user = UserProfiles(user).add_profile(default="Cliente")
        user.save()

        return user
