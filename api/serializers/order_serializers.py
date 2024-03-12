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


class OrderDetailSerializer(serializers.ModelSerializer):
    pickup_point = serializers.SlugRelatedField(read_only=True, slug_field="name")
    delivery_point = serializers.SlugRelatedField(read_only=True, slug_field="name")
    employee = EmployeeSerializer(read_only=True, many=False, )
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
            "employee",
            "status",
            "plan",
        ]
