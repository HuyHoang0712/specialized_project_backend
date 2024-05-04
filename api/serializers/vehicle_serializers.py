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

    def to_representation(self, instance):
        return {
            "license_plate": instance.license_plate,
            "capacity": instance.capacity,
            "fuel_consumption_level": instance.fuel_consumption_level,
            "status": instance.status,
            "brand": instance.brand,
            "driver": instance.driver.name,
        }


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
