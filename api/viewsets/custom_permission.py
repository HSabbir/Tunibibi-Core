from django.contrib.auth.models import User
from rest_framework import permissions


class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        if User.objects.filter(username=request.user.username, groups__name='Buyer').exists():
            return True
        else:
            return False