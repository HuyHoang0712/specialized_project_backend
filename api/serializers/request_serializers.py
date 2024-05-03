from rest_framework import serializers
from api.models import *


class RequestSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = Requests
        fields = (
            "id",
            "title",
            "description",
            "date_time",
            "status",
            "label",
            "creator",
            "order",
            "vehicle",
            "warehouse",
        )
