from django.urls import path, include
from rest_framework import routers
from api.views.auth_view import *
from api.views.employee_view import *
from api.views.warehouse_view import *
from api.views.notification_view import *
from api.views.has_notification_view import *
from api.views.delivery_point_view import *
from api.views.order_view import *
from api.views.issue_view import *
from rest_framework_simplejwt.views import TokenRefreshView

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
    path("v1/", include(router.urls)),
    path("auth/login", UserLoginView.as_view(), name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh_view"),
]
