from rest_framework import serializers
from api.models import *


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ("id", "name", "address", "longitude", "latitude")
