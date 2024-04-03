from rest_framework import serializers
from api.models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "address", "longitude", "latitude"]


# class CreateCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ["name", "address", "longitude", "latitude"]
