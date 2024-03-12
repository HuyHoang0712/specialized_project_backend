from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "role", "status"]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "address", "longitude", "latitude", "status"]


@admin.register(TransportationPlan)
class TransportationPlan(admin.ModelAdmin):
    list_display = ["id", "date"]


admin.site.register(Notification)


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
        "pickup_id",
        "employee_id",
        "plan_id",
    ]


@admin.register(DeliveryPoint)
class DeliveryPoint(admin.ModelAdmin):
    list_display = ["name", "address", "longitude", "latitude"]


admin.site.register(Issue)
admin.site.register(HasNotification)
