from rest_framework import serializers
from api.models import *


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
