from rest_framework import permissions
from settings import local_settings
from station_auth.models import StationToken

import jwt
from jwt import DecodeError, ExpiredSignature
token_secret = local_settings.SCREEN_TOKEN_SECRET
token_key_word_origin = local_settings.SCREEN_TOKEN_KEY_WORD


class IsAuthenticatedScreen(permissions.BasePermission):

    def has_permission(self, request, view):
        if "HTTP_BIT_TOKEN" in request.META:
            token_key_word = request.META["HTTP_BIT_TOKEN"].split()[0]
            t = request.META["HTTP_BIT_TOKEN"].split()[1]
            if token_key_word == token_key_word_origin:
                try:
                    token = jwt.decode(t, token_secret)
                except DecodeError:
                    return {"message": "Token invalid!"}, 401
                except ExpiredSignature:
                    return {"message": "Token has expired"}, 401

                token_obj = StationToken.objects.filter(station_id=token["sub"], token=t).first()
                if token_obj:
                    return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_admin:
            return True
        return False
