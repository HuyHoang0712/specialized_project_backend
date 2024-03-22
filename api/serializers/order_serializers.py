from rest_framework import serializers
from api.models import *
from .employee_serializers import *
from .vehicle_serializers import *


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
            "vehicle",
            "status",
            "plan",
        )

    def to_representation(self, instance):
        issues = Issue.objects.filter(order_id=instance.id).count()
        return {
            "id": instance.id,
            "ship_code": instance.ship_code,
            "date": instance.date,
            "time_in": instance.time_in,
            "payload": instance.payload,
            "pickup_point": instance.pickup_point.name,
            "delivery_point": instance.delivery_point.name,
            "vehicle": instance.vehicle.license_plate if instance.vehicle else None,
            "status": instance.status,
            "issues_count": issues
        }


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "ship_code",
            "date",
            "time_in",
            "payload",
            "pickup_point",
            "delivery_point",
            "vehicle",
            "status",
            "plan",
        ]

    def to_representation(self, instance):
        vehicle = VehicleDetailSerializer(instance.vehicle, many=False, read_only=True)
        return {
            "id": instance.id,
            "ship_code": instance.ship_code,
            "date": instance.date,
            "time_in": instance.time_in,
            "payload": instance.payload,
            "pickup_point": instance.pickup_point if type(
                instance.pickup_point) == "String" else instance.pickup_point.name,
            "delivery_point": instance.delivery_point if type(
                instance.delivery_point) == "String" else instance.delivery_point.name,
            "vehicle": vehicle.data,
            "status": instance.status,

        }
