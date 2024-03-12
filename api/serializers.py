from rest_framework import serializers
from .models import *


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "name", "date_of_birth", "role", "email", "status")


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ("id", "name", "address", "longitude", "latitude")


class TransportationPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationPlan
        fields = ("id", "date")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "date_time", "employess")


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "license_plate",
            "capacity",
            "fuel_consumption_level",
            "status",
            "brand",
            "driver",
        )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name", "address", "longitude", "latitude")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "ship_code",
            "date",
            "time_in",
            "payload",
            "pickup_point",
            "delivery_point",
            "employee",
            "status",
            "plan",
        )


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = (
            "id",
            "title",
            "description",
            "date_time",
            "status",
            "label",
            "creator",
            "order",
            "vehicle",
            "warehouse",
        )
