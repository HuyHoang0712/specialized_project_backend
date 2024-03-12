from rest_framework import serializers
from api.models import *


class IssueSerializer(serializers.ModelSerializer):
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
            "order",
            "vehicle",
            "warehouse",
        )
