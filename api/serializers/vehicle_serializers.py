from rest_framework import serializers
from api.models import *
from .employee_serializers import *


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


class VehicleDetailSerializer(serializers.ModelSerializer):
    driver = EmployeeSerializer(
        read_only=True,
        many=False,
    )

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
