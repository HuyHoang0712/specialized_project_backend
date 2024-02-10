from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from  rest_framework.decorators import action
from .models import *
from .serializers import *

# Create your views here.


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['POST'])
    def get_user(self, request, pk=None):
        if 'username' in request.data:
            user_instance = Employee.objects.get(username=request.data['username'])
            serializer = EmployeeSerializer(user_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        error = "Something is wrong!"
        return Response(error, status=status.HTTP_404_NOT_FOUND)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class DeliveryPointViewSet(viewsets.ModelViewSet):
    queryset = DeliveryPoint.objects.all()
    serializer_class = DeliveryPointSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class HasNotificationViewSet(viewsets.ModelViewSet):
    queryset = HasNotification.objects.all()
    serializer_class = HasNotificationSerializer
