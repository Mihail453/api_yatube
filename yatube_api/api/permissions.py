from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование и удаление только автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        """
        Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем пользователям
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)
