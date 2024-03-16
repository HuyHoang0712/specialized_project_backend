from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Employee)
# admin.site.register(Warehouse)
# admin.site.register(TransportationPlan)
admin.site.register(Notification)
# admin.site.register(Vehicle)
# admin.site.register(Customer)
# admin.site.register(Order)
admin.site.register(Issue)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "role", "status"]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "address"]


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
