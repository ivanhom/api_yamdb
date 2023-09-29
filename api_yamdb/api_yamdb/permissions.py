from rest_framework import permissions


class IsAuthorOrJustReading(permissions.BasePermission):
    """
    Разрешает модификацию объекта только его владельцу.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                )
