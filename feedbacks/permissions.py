from rest_framework import permissions
from settings import local_settings
from station_auth.models import StationToken
token_key_word_origin = local_settings.SCREEN_TOKEN_SECRET


class IsAuthenticatedScreen(permissions.BasePermission):
    def has_permission(self, request, view):

        if "HTTP_BIT_TOKEN" in request.META:
            token_key_word = request.META["HTTP_BIT_TOKEN"].split()[0]
            token = request.META["HTTP_BIT_TOKEN"].split()[1]

            if token_key_word == token_key_word_origin and token not in [None, ""]:
                token_obj = StationToken.objects.filter(key=token).first()
                if token_obj:
                    return True
        return False
