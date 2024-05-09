from rest_framework import serializers
from api.models import *
from datetime import datetime, timezone
from ..serializers.employee_serializers import *


class IssueSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(read_only=True, slug_field="name")

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

class VehicleIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"

    def to_representation(self, instance):
        vehicle_issue = IssueVehicle.objects.get(request_id=instance.id)

        return {
            "id": instance.id,
            "title": instance.title,
            "label": instance.label,
            "description": instance.description,
            "date_time": instance.date_time,
            "status": instance.status,
            "creator": instance.creator.name,
            "vehicle_id": vehicle_issue.vehicle_id.license_plate,
            "cost": vehicle_issue.cost,
        }
