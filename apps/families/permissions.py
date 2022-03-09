from rest_framework import permissions


class UserIsFamilyMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.families.filter(id=view.kwargs.get("family_id")).exists()
