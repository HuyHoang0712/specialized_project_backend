from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=32)
    status = models.PositiveSmallIntegerField(default=1)


class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    status = models.PositiveSmallIntegerField(default=1)


class TransportationPlan(models.Model):
    date = models.DateField(default=timezone.now())


class Notification(models.Model):
    title = models.CharField(max_length=32)
    message = models.TextField()
    date_time = models.DateTimeField()


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=32, primary_key=True)
    capacity = models.IntegerField()
    fuel_consumption_level = models.IntegerField()
    status = models.PositiveSmallIntegerField(default=1)
    driver_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)


class DeliveryPoint(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)


class Order(models.Model):
    ship_code = models.CharField(max_length=32)
    date = models.DateField(default=timezone.now())
    status = models.PositiveSmallIntegerField(default=2)
    time_in = models.TimeField()
    payload = models.CharField(max_length=32)
    pickup_id = models.ForeignKey(DeliveryPoint, on_delete=models.SET_NULL, null=True,  related_name="pickup_id")
    delivery_id = models.ForeignKey(DeliveryPoint, on_delete=models.SET_NULL, null=True, related_name="delivery_id")
    employee_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    plan_id = models.ForeignKey(
        TransportationPlan, on_delete=models.SET_NULL, null=True
    )


class Issue(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    date_time = models.DateTimeField()
    status = models.PositiveSmallIntegerField(default=2)
    label = models.CharField(max_length=32)
    creator_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    vehicle_license_plate = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True
    )
    warehouse_id = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)


class HasNotification(models.Model):
    notification_id = models.ForeignKey(
        Notification, on_delete=models.SET_NULL, null=True
    )
    employee_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
