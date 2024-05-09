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
