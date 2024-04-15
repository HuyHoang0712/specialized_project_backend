from rest_framework import serializers
from api.models import *
from datetime import datetime


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


def generate_employee_id():
    # Get the current year
    current_year = datetime.now().year

    # Get the total number of employees
    total_employees = Employee.objects.count()

    # Generate the employee id
    employee_id = str(current_year)[2:] + str(total_employees + 1).zfill(4)

    return employee_id


class CreateEmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    Dob = serializers.DateField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, max_length=12)
    group = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        goups = Group.objects.get(name=validated_data["group"])
        user.groups.add(goups)
        employee = Employee.objects.create(
            id=generate_employee_id(),
            user=user,
            name=validated_data["first_name"].join(" ", validated_data["last_name"]),
            email=validated_data["email"],
            date_of_birth=validated_data["Dob"],
            phone=validated_data["phone"],
        )
        user.save()
        employee.save()
        return employee
