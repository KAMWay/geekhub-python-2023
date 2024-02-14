from rest_framework.permissions import BasePermission, SAFE_METHODS


class DefaultPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return request.method in SAFE_METHODS
