from rest_framework import serializers
from api.models import *
from datetime import datetime, timezone
from ..serializers.employee_serializers import *


class IssueSerializer(serializers.ModelSerializer):
    # creator = serializers.SlugRelatedField(read_only=True, slug_field="name")

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

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "description": instance.description,
            "date_time": instance.date_time,
            "status": instance.status,
            "label": instance.label,
            "creator": instance.creator.name,
        }


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

    def create(self, validated_data, vehicle_id, cost):
        issue = Issue.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            label=validated_data["label"],
            creator=validated_data["creator"],
        )
        issue.save()
        vehicle_issue = IssueVehicle.objects.create(
            request_id=issue,
            vehicle_id=Vehicle.objects.get(license_plate=vehicle_id),
            cost=cost,
        )
        vehicle_issue.save()
        create_serializers = VehicleIssueSerializer(issue)
        return create_serializers.data
