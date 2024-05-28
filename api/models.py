from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime

# Create your models here.

ORDER_STATUS = [(0, "Pending"), (1, "In Progress"), (2, "Completed"), (3, "Canceled")]

VEHICLE_STATUS = [
    (0, "Repairing"),
    (1, "Delivering"),
    (2, "Available"),
    (3, "Unavailable"),
]

EMPLOYEE_STATUS = [
    (2, "Available"),
    (3, "On Leave"),
]

ISSUE_STATUS = [
    (0, "Pending"),
    (2, "Approved"),
    (3, "Denied"),
    (4, "Canceled"),
]
NOTIFICATION_TYPE = [(0, 'general'), (1, 'order'), (2, 'issue')]


class Employee(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True)
    status = models.IntegerField(
        default=2, choices=EMPLOYEE_STATUS
    )
    objects = models.Manager()

    class Meta:
        permissions = [
            (
                "supervisor",
                "can act as a supervisor",
            ),
            (
                "driver",
                "can act as a driver",
            ),
        ]


class TransportationPlan(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    objects = models.Manager()


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=32, primary_key=True)
    capacity = models.IntegerField(null=False)
    fuel_consumption_level = models.IntegerField(null=False)
    status = models.IntegerField(default=2, choices=VEHICLE_STATUS)
    brand = models.CharField(default=None, max_length=32, blank=True)
    driver = models.OneToOneField(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )
    objects = models.Manager()


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    address = models.TextField()
    longitude = models.CharField(max_length=254)
    latitude = models.CharField(max_length=254)
    objects = models.Manager()


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
    status = models.IntegerField(default=0, choices=ORDER_STATUS)
    plan = models.ForeignKey(TransportationPlan, on_delete=models.SET_NULL, null=True)

    objects = models.Manager()


class Issue(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=254)
    label = models.CharField(max_length=254)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, choices=ISSUE_STATUS)
    creator = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = models.Manager()


class IssueVehicle(models.Model):
    request_id = models.OneToOneField(Issue, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    cost = models.IntegerField(default=0)
    objects = models.Manager()


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(default=0, choices=NOTIFICATION_TYPE)
    sender_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    send_datetime = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class HasNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    objects = models.Manager()


class NotificationOrder(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    objects = models.Manager()


class NotificationIssue(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    objects = models.Manager()
