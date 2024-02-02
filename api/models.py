from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    password = models.CharField(max_length=16)
    username = models.CharField(max_length=50)


class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)
    status = models.CharField(max_length=32)


class Notification(models.Model):
    title = models.CharField(max_length=32)
    message = models.TextField()
    date_time = models.DateTimeField()


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=32, primary_key=True)
    capacity = models.IntegerField()
    fuel_consumption_level = models.IntegerField()
    status = models.CharField(max_length=32)
    driver_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)


class DeliveryPoint(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    longitude = models.CharField(max_length=32)
    latitude = models.CharField(max_length=32)


class Order(models.Model):
    ship_code = models.CharField(max_length=32)
    date = models.DateField()
    time_in = models.TimeField()
    payload = models.CharField(max_length=32)
    pickup_id = models.ForeignKey(DeliveryPoint, on_delete=models.SET_NULL, null=True)
    # delivery_id = models.ForeignKey(DeliveryPoint, on_delete=models.SET_NULL, null=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)


class Issue(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    date_time = models.DateTimeField()
    status = models.CharField(max_length=32)
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
