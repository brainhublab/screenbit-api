from rest_framework import permissions
from settings import local_settings
from .models import Feedback
worker_token = local_settings.WORKER_TOKEN


class IsAdminUserOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj, Feedback):
            # only user can edit himself
            if request.user.is_admin:
                return True
            else:
                return False


class IsAuthenticatedWorker(permissions.BasePermission):

    def has_permission(self, request, view):
        if "HTTP_AUTHORIZATION" in request.META:
            print(request.META["HTTP_AUTHORIZATION"])
            t = request.META["HTTP_AUTHORIZATION"].split()[1]
            if t == worker_token:
                return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_admin:
            return True
        return False
