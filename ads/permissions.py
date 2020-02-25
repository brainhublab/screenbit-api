from rest_framework import permissions
from .models import Ad


class IsAdminUserOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj, Ad):
            # only user can edit himself
            if obj.creator == request.user:
                return True
            elif request.user.is_admin:
                return True
            else:
                return False
