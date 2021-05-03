""" Handler for tokens """
import jwt

from django.conf import settings
from django.utils import timezone

from ..models.auth import Auth
from ..models.user import User


class TokenHandler:
    """ Controls all the token functionalities for sessions """

    def get_payload(self, request):
        """ Returns token payload if is enabled or active.

        Parameter
        ---------

        request: dict
            Request information

        Return
        ------

        dict - Token if it is active or enabled, else None

        """
        header = request.headers.get("Authorization", None)
        if (not header or len(header.split(" ")) != 2 or
                header.split(" ")[0].lower() != "bearer"):
            return None, None

        try:
            token = jwt.decode(header.split(
                " ")[1], settings.SECRET_KEY, algorithms='HS256')
        except jwt.InvalidTokenError:
            return None, None

        expiration_date = timezone.strptime(token['expiration_date'],
            '%Y-%m-%d %H:%M:%S.%f')

        db_token = Auth.objects.filter(token=header.split(" ")[1]).first()

        if (expiration_date < timezone.now() or not db_token or
                db_token.is_disabled):
            return None, None

        user = User.objects.filter(
            email=token["email"], is_active=True).first()

        if not user:
            return None, None

        return token, user

    def is_owner(self, token_email, request_child):
        """ Asserts if token owner is also the request child.

        Parameters
        ----------

        token_email: str
            Email value inside token

        request_child: str
            Request child to be asserted

        Return
        ------

        bool - True if data is the same

        """
        # pylint: disable=no-self-use
        return token_email == request_child

    def has_permissions(self, profiles, user):
        return user.profile.filter(profile__in=profiles).exists()
