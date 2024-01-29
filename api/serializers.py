from rest_framework import serializers
from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "name", "date_of_birth", "role", "status")


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ("id", "name", "address", "longitude", "latitude", "status")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "date_time")


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "license_plate",
            "capacity",
            "fuel_consumption_level",
            "status",
            "driver_id",
        )


class DeliveryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPoint
        fields = ("name", "address", "longitude", "latitude")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("ship_code", "date", "time_in", "payload", "pickup_id", "employee_id")


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = (
            "title",
            "description",
            "date_time",
            "status",
            "label",
            "creator_id",
            "order_id",
            "vehicle_license_plate",
            "warehouse_id",
        )


class HasNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HasNotification
        fields = ("notification_id", "employee_id")
