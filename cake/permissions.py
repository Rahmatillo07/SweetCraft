from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and
            hasattr(request.user, "role") and
            request.user.role == "admin"
        )


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated and hasattr(request.user, "role") and request.user.role == "admin":
            return True

        if request.method == "DELETE":
            return False

        return obj.user == request.user


class AdminRequiredPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == "admin":
            return True

        return False
