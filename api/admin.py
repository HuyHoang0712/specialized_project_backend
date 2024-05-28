from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(IssueVehicle)
class IssueVehicleAdmin(admin.ModelAdmin):
    list_display = ["vehicle_id", "request_id", "cost"]

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "label", "creator"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "status"]


@admin.register(TransportationPlan)
class TransportationPlan(admin.ModelAdmin):
    list_display = ["id", "date"]


@admin.register(Vehicle)
class Vehicle(admin.ModelAdmin):
    list_display = [
        "license_plate",
        "capacity",
        "fuel_consumption_level",
        "status",
        "driver_id",
    ]


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = [
        "id",
        "ship_code",
        "date",
        "time_in",
        "payload",
        "pickup_point_id",
        "delivery_point_id",
        "vehicle",
        "plan_id",
    ]


@admin.register(Customer)
class Customer(admin.ModelAdmin):
    list_display = ["id", "name", "address", "longitude", "latitude"]


@admin.register(Notification)
class Notification(admin.ModelAdmin):
    list_display = ["id", "sender_id", "description", "send_datetime"]

@admin.register(HasNotification)
class HasNotification(admin.ModelAdmin):
    list_display = ["employee_id", "notification_id", "is_read"]

@admin.register(NotificationIssue)
class NotificationIssue(admin.ModelAdmin):
    list_display = ["issue_id", "notification_id"]

@admin.register(NotificationOrder)
class NotificationOrder(admin.ModelAdmin):
    list_display = ["order_id", "notification_id"]
