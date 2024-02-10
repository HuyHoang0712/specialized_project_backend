from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from .models import *
from .serializers import *
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import permission_required

###
from rest_framework.decorators import action
from rest_framework.response import Response


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


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_employee", raise_exception=True),
        permission_required("api.add_employee", raise_exception=True),
        permission_required("api.change_employee", raise_exception=True),
        permission_required("api.delete_employee", raise_exception=True),
    )

    # def get_queryset(self):
    #     return Employee.objects.all()


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_warehouse", raise_exception=True),
        permission_required("api.add_warehouse", raise_exception=True),
        permission_required("api.change_warehouse", raise_exception=True),
        permission_required("api.delete_warehouse", raise_exception=True),
    )

    # def get_queryset(self):
    #     return Warehouse.objects.all()


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = (BasicAuthentication,)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_vehicle", raise_exception=True),
        permission_required("api.add_vehicle", raise_exception=True),
        permission_required("api.change_vehicle", raise_exception=True),
        permission_required("api.delete_vehicle", raise_exception=True),
    )


class DeliveryPointViewSet(viewsets.ModelViewSet):
    queryset = DeliveryPoint.objects.all()
    serializer_class = DeliveryPointSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_deliverypoint", raise_exception=True),
        permission_required("api.add_deliverypoint", raise_exception=True),
        permission_required("api.change_deliverypoint", raise_exception=True),
        permission_required("api.delete_deliverypoint", raise_exception=True),
    )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (BasicAuthentication,)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    authentication_classes = (BasicAuthentication,)


class HasNotificationViewSet(viewsets.ModelViewSet):
    queryset = HasNotification.objects.all()
    serializer_class = HasNotificationSerializer
    authentication_classes = (BasicAuthentication,)
