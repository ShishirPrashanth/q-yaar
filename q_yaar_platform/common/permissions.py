from rest_framework import permissions


class ActivePermission(permissions.BasePermission):
    """
    Global permission check for user is active.
    """

    message = "inactive user"

    def has_permission(self, request, view):
        return request.user.is_anonymous or request.user.is_active
