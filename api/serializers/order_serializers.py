from rest_framework import serializers
from api.models import *
from .employee_serializers import *
from .vehicle_serializers import *


class OrderSerializer(serializers.ModelSerializer):
    pickup_point = serializers.SlugRelatedField(read_only=True, slug_field="name")
    delivery_point = serializers.SlugRelatedField(read_only=True, slug_field="name")
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
            "vehicle": instance.vehicle.license_plate,
            "status": instance.status,
            "issues_count": issues
            # "plan": instance.plan.id,
        }


class OrderDetailSerializer(serializers.ModelSerializer):
    pickup_point = serializers.SlugRelatedField(read_only=True, slug_field="name")
    delivery_point = serializers.SlugRelatedField(read_only=True, slug_field="name")
    vehicle = VehicleDetailSerializer(
        read_only=True,
        many=False,
    )

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
