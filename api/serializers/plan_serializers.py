from rest_framework import serializers
from api.models import *


class TransportationPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationPlan
        fields = ("id", "date")