from rest_framework import permissions
from account.models import *

class Students(permissions.BasePermission):
    message = 'You are not allowed to access'

    def has_permission(self, request, view):
        if request.user.is_student:
            return True
        else:
            return False

class TestDetails(permissions.BasePermission):
    message = 'You are not allowed to access'

    def has_permission(self, request, view):
        if request.method=='GET':
            return True
        test_email=McqExam.objects.get(pk=view.kwargs['pk']).teacher
        print(test_email)
        email=request.user.email
        print(email)
        if str(test_email)==str(email):
            return True
        else:
            return False
