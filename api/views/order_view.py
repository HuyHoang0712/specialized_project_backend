from .backend import *
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from dateutil.relativedelta import relativedelta

today = datetime.today().strftime("%Y-%m-%d")


def create_notification(order, sender_id, description):
    receiver_ids = list(
        Employee.objects.filter(user__groups__name="Facillities Manager").values_list("id", flat=True))
    receiver_ids = list(set(receiver_ids + [order.vehicle.driver.id]))
    sender_id = Employee.objects.get(user__id=sender_id).id
    noti_serializer = CreateNotificationSerializer(
        data={
            "type": 1,
            "sender_id": sender_id,
            "description": description,
            "receiver_ids": receiver_ids,
            "order": order.id,
        }
    )
    if noti_serializer.is_valid():
        noti_serializer.create(noti_serializer.validated_data)
    else:
        print(noti_serializer.errors)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["get"])
    def get_order_summary_of_customer(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        customer_id = request.query_params["customer_id"]
        # Calculate the date 6 months ago
        six_months_ago = timezone.now() - relativedelta(months=6)

        # Filter the orders from the last 6 months
        queryset = Order.objects.filter(
            date__gte=six_months_ago, delivery_point_id=customer_id
        )

        # Annotate the queryset with the count of each status for each month
        order_summary = (
            queryset.annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(
                pending=Count("status", filter=models.Q(status=0)),
                in_progress=Count("status", filter=models.Q(status=1)),
                completed=Count("status", filter=models.Q(status=2)),
                canceled=Count("status", filter=models.Q(status=3)),
            )
            .order_by("month")
        )

        return Response(order_summary, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_order_summary_of_vehicle(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vehicle_id = request.query_params["vehicle_id"]
        # Calculate the date 6 months ago
        six_months_ago = timezone.now() - relativedelta(months=6)

        # Filter the orders from the last 6 months
        queryset = Order.objects.filter(date__gte=six_months_ago, vehicle_id=vehicle_id)
        # Filter the orders from the last 6 months
        queryset = Order.objects.filter(date__gte=six_months_ago, vehicle_id=vehicle_id)

        # Annotate the queryset with the count of each status for each month
        order_summary = (
            queryset.annotate(month=ExtractMonth("date"))
            .values("month")
            .annotate(
                pending=Count("status", filter=models.Q(status=0)),
                in_progress=Count("status", filter=models.Q(status=1)),
                completed=Count("status", filter=models.Q(status=2)),
                canceled=Count("status", filter=models.Q(status=3)),
            )
            .order_by("month")
        )

        return Response(order_summary, status=status.HTTP_200_OK)
        return Response(order_summary, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_orders_by_date(self, request, pk=None):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qr_date = request.query_params["date"]
        queryset = Order.objects.filter(date=qr_date)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get_orders_in_plan")
    def get_all_orders_in_transportation_plan(self, request, pk=None):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qr_plan = request.query_params["plan_id"]
        queryset = Order.objects.filter(plan=qr_plan)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get_order_by_id")
    def get_order_by_id(self, request):
        qr_id = request.query_params["id"]
        queryset = Order.objects.get(id=qr_id)
        if "flag" in request.query_params:
            qr_flag = request.query_params["flag"]
            if qr_flag == "driver":
                serializer = OrderDetailForDriverSerializer(queryset)
                return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = OrderDetailSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["put"],
        permission_classes=[
            permission_required("api.change_order", raise_exception=True)
        ],
    )
    def update_order(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qr_id = request.query_params["id"]
        order = Order.objects.get(id=qr_id)
        if order:
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res_serializer = OrderDetailSerializer(order)
                # Sent notification
                sender_id = request.user.id
                description = f"Order {order.id} detials have been updated."
                create_notification(order, sender_id, description)

                return Response(res_serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"detail": "The updated information is invalid! Please try again!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Order is not founded!"}, status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=False, methods=["put"])
    def update_order_status(self, request):
        qr_id = request.data["id"]
        order = Order.objects.get(id=qr_id)
        if order:
            res_serializer = OrderDetailForDriverSerializer(
                order, data=request.data, partial=True
            )
            if res_serializer.is_valid():
                res_serializer.save()
                # Sent notification
                sender_id = request.user.id
                description = f"Order {order.id} has been updated status."
                create_notification(order, sender_id, description)
                return Response(res_serializer.data, status=status.HTTP_200_OK)
            return Response(
                {"detail": "The updated information is invalid! Please try again!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Order is not founded!"}, status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=False, methods=["get"])
    def get_orders_of_delivery_point(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qr_id = request.query_params["delivery_point"]
        queryset = Order.objects.filter(delivery_point=qr_id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_orders_of_vehicle(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vehicle_id = request.query_params["vehicle"]
        queryset = Order.objects.filter(vehicle=vehicle_id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_recent_orders_coordinates(self, request, pk=None):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qr_date = request.query_params["date"]
        queryset = Order.objects.filter(date=qr_date)
        orders = OrderCoordinateSerializer(queryset, many=True)
        set_of_coordinates = []
        for order in orders.data:
            coordinates = [
                order["delivery_point"]["longitude"],
                order["delivery_point"]["latitude"],
            ]
            if coordinates not in set_of_coordinates:
                set_of_coordinates += [coordinates]
        return Response(set_of_coordinates, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_order_coordinates_by_id(self, request, pk=None):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        qr_id = request.query_params["id"]
        queryset = Order.objects.get(id=qr_id)
        order = OrderCoordinateSerializer(queryset)
        pickup_point_coordinates = [
            order.data["pickup_point"]["longitude"],
            order.data["pickup_point"]["latitude"],
        ]
        delivery_point_coordinates = [
            order.data["delivery_point"]["longitude"],
            order.data["delivery_point"]["latitude"],
        ]
        set_of_coordinates = [pickup_point_coordinates, delivery_point_coordinates]
        return Response(set_of_coordinates, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_current_orders(self, request):
        user_id = request.user.id
        profile = Employee.objects.get(user__id=user_id)
        queryset = Order.objects.filter(vehicle__driver__id=profile.id)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
