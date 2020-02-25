from rest_framework import permissions
from .models import Station


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj, Station):
            if request.user.is_admin:
                return True
            else:
                return False
