from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register("employees", EmployeeViewSet)
router.register("warehouses", WarehouseViewSet)
router.register("notifications", NotificationViewSet)
router.register("vehicles", NotificationViewSet)
router.register("delivery_points", DeliveryPointViewSet)
router.register("orders", OrderViewSet)
router.register("issues", IssueViewSet)
router.register("has_notification", HasNotificationViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
