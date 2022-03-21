from rest_framework import permissions


class UserHasFamilyAccessPermission(permissions.BasePermission):
    message = "User must be a member of the request family"

    def has_permission(self, request, view):
        family_id = request.data.get("family", None)

        if family_id:
            return request.user.families.filter(id=family_id).exists()
        else:
            self.message = "Family is required"
            return False


class UserHasFamilyAccessObjectPermission(permissions.BasePermission):
    message = "User doesn't have access to this purchase"

    # def has_permission(self, request, view):

        # return request.user.families.filter(id=).exists()

    def has_object_permission(self, request, view, obj):
        print(obj.family.id)
        return request.user.families.filter(id=obj.family.id).exists()
