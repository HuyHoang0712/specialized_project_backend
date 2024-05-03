from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

# Create your models here.

STATUS_ORDER = [(0, "Pending"), (1, "In Progress"), (2, "Completed"), (3, "Cancel")]

STATUS_EMPL_VEHICLE = [
    (0, "Available"),
    (1, "Busy"),
    (2, "On Break"),
]


class Employee(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    status = models.IntegerField(
        default=STATUS_EMPL_VEHICLE[0][0], choices=STATUS_EMPL_VEHICLE
    )


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)


class TransportationPlan(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    message = models.TextField()
    date_time = models.DateTimeField()
    employees = models.ManyToManyField(Employee)


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=32, primary_key=True)
    capacity = models.IntegerField(null=False)
    fuel_consumption_level = models.IntegerField(null=False)
    status = models.IntegerField(
        default=VEHICLE_STATUS[1][0], choices=VEHICLE_STATUS
    )
    brand = models.CharField(default=None, max_length=32, blank=True)
    driver = models.OneToOneField(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    address = models.TextField()
    longitude = models.CharField(max_length=254)
    latitude = models.CharField(max_length=254)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    ship_code = models.CharField(max_length=32)
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField()
    payload = models.IntegerField()
    pickup_point = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name="pickup_point"
    )
    delivery_point = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, related_name="delivery_point"
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(default=STATUS_ORDER[0][0], choices=STATUS_ORDER)
    plan = models.ForeignKey(TransportationPlan, on_delete=models.SET_NULL, null=True)


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=254)
    description = models.TextField()
    date_time = models.DateTimeField()
    status = models.IntegerField(default=STATUS_ORDER[0][0], choices=STATUS_ORDER)
    label = models.CharField(max_length=254)
    creator = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )

class IssueVehicle(models.Model):
    request_id = models.OneToOneField(Issue, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)