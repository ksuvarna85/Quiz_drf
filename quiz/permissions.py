from rest_framework import permissions

class Students(permissions.BasePermission):
    message = 'You are not allowed to access'

    def has_permission(self, request, view):
        if request.user.is_student:
            return True
        else:
            return False
