from rest_framework import serializers
from api.models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "user", "name", "date_of_birth", "email", "status")
