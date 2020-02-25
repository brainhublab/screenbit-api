from rest_framework import permissions
import settings
import importlib

from authentication.models import User

from screenbit_core.models import Image, File


def load(path):
    parts = path.split('.')
    class_name = parts.pop()
    module_name = '.'.join(parts)
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    return class_


DEFAULT_PERMISSION_CLASSES = list(map(load, settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']))


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly,
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsAuthenticatedAndVerified(permissions.IsAuthenticated):
    """Is authenticated and verified"""
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.is_verified_email

    def has_object_permission(self, request, view, obj):
        is_authenticated = super().has_object_permission(request, view, obj)
        return is_authenticated and request.user.is_verified_email


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if isinstance(obj, User):
            # only user can edit himself
            if obj == request.user:
                return True
            else:
                return False

        if isinstance(obj, Image):
            author = getattr(obj.content_object, 'author', None)
            if author and not author.is_anonymous:
                return author.id == request.user.id
        if isinstance(obj, File):
            author = getattr(obj.content_object, 'author', None)
            if author and not author.is_anonymous:
                return author.id == request.user.id

        # no.
        return False


class IsOwnerOrReadOnly(IsOwner):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return super(IsOwnerOrReadOnly, self).has_object_permission(request, view, obj)
