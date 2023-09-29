from rest_framework import permissions


class IsAuthorOrJustReading(permissions.BasePermission):
    """Разрешает модификацию объекта только его владельцу."""


    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                )

class IsAdminOrReadOnly(permissions.BasePermission):
    """Для работы с Genres и Categories."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'admin'
        return False
