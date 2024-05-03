from rest_framework import serializers
from api.models import *


class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="name")
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    vehicle = serializers.PrimaryKeyRelatedField(read_only=True)
    warehouse = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = Issue
        fields = (
            "id",
            "title",
            "description",
            "date_time",
            "status",
            "label",
            "creator",
        )
