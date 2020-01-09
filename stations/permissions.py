from rest_framework import permissions

from .models import Screen


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # TODO
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj, Screen):
            return obj.owner.id == request.user.id
        # no.
        return False
