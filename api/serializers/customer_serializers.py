from rest_framework import serializers
from api.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "address", "longitude", "latitude"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "address": instance.address,
        }

# class CreateCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ["name", "address", "longitude", "latitude"]
