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


class CreateIssueSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=254)
    label = serializers.CharField(max_length=254)
    description = serializers.CharField()
    creator = serializers.CharField(max_length=254)

    def create(self, validated_data):
        now = datetime.now()
        employee = Employee.objects.get(id=validated_data["creator"])
        print(employee)

        issue = Issue.objects.create(
            title=validated_data["title"],
            label=validated_data["label"],
            description=validated_data["description"],
            date_time=now,
            creator=employee,
        )
        issue.save()
        return issue


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
            "date_time": datetime.fromisoformat(issue.data["date_time"][:-1])
            .astimezone(timezone.utc)
            .strftime("%Y-%m-%d %H:%M:%S"),
            "status": issue.data["status"],
            "creator": issue.data["creator"],
            "vehicle_id": instance.vehicle_id.license_plate,
            "cost": instance.cost,
        }
