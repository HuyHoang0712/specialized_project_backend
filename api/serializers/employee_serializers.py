from rest_framework import serializers
from api.models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "name", "date_of_birth", "email", "status")

    def to_representation(self, instance):
        role = instance.user.groups.all()[0].name if instance.user.groups.all() else "Employee"
        return {
            "id": instance.id,
            "role": role,
            "name": instance.name,
            "date_of_birth": instance.date_of_birth,
            "email": instance.email,
            "status": instance.status,
        }


class CreateEmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    Dob = serializers.DateField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, max_length=12)
    group = serializers.CharField(required=True)

    def create(self, validated_data):
        first_name, last_name = validated_data["name"].split(" ", 1)
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=first_name,
            last_name=last_name,
        )
        goups = Group.objects.get(name=validated_data["group"])
        user.groups.add(goups)
        user.save()
        employee = Employee.objects.create(
            id=validated_data["id"],
            user=user,
            name=validated_data["name"],
            email=validated_data["email"],
            date_of_birth=validated_data["Dob"],
            phone=validated_data["phone"],
        )
        employee.save()
        return employee
