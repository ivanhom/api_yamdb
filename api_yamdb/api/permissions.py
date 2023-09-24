from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать
    его только владельцам объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(BasePermission):
    """
    Разрешение на уровне запроса, предоставляющее
    пользователям только право на чтение.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
