from django.urls import path, include
from rest_framework import routers
from api.views.auth_view import *
from api.views.employee_view import *
from api.views.notification_view import *
from api.views.customer_view import *
from api.views.order_view import *
from api.views.issue_view import *
from api.views.plan_view import *
from api.views.vehicle_view import *
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register("employees", EmployeeViewSet)
router.register("notifications", NotificationViewSet)
router.register("vehicles", VehicleViewSet)
router.register("customers", CustomerViewSet)
router.register("orders", OrderViewSet)
router.register("issues", IssueViewSet)
router.register("plans", PlanViewSet)
router.register("profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("auth/login/supervisor", SupervisorLoginView.as_view(), name="supervisor_login"),
    path("auth/login/employee", EmployeeLoginView.as_view(), name="employee_login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh_view"),
]
