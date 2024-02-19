from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path("token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh_view')
]
