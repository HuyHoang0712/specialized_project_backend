from rest_framework import viewsets, permissions, exceptions, status
from rest_framework.decorators import action, APIView
from django.conf import settings
from api.models import *
from api.serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import permission_required


# Create your views here.
def permission_required(permission_name, raise_exception=False):
    class PermissionRequired(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user.has_perm(permission_name):
                if raise_exception:
                    raise exceptions.PermissionDenied("Don't have permission")
                return False
            return True

    return PermissionRequired
