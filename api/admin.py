from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "role", "status"]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "address", "longitude", "latitude"]


admin.site.register(Notification)
admin.site.register(Vehicle)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Issue)
