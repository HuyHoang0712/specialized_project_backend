from rest_framework import serializers
from api.models import *
from datetime import datetime, timezone


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

    def to_representation(self, instance):
        issue = IssueSerializer(instance.request_id, many=False, read_only=True)

        return {
            "id": issue.data["id"],
            "title": issue.data["title"],
            "label": issue.data["label"],
            "description": issue.data["description"],
            "date_time": datetime.fromisoformat(issue.data['date_time'][:-1]).astimezone(timezone.utc).strftime(
                '%Y-%m-%d %H:%M:%S'),
            "status": issue.data["status"],
            "creator": issue.data["creator"],
            "vehicle_id": instance.vehicle_id.license_plate,
            "cost": instance.cost,
        }
