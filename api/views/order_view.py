from api.models import Order
from api.serializers import OrderSerializer
from .backend import *
from datetime import datetime
import json

today = datetime.today().strftime("%Y-%m-%d")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # authentication_classes = (JWTAuthentication,)
    authentication_classes = ()
    permission_classes = ()

    @action(detail=False, methods=["post"])
    def get_orders_by_date(self, request, pk=None):
        qr_date = request.data["date"]
        query_data = Order.objects.filter(date=qr_date)
        data = []
        pickup_point = ""
        delivery_point = ""
        employee_id = ""
        for order in query_data:
            # Handle null data
            if order.pickup_id:
                pickup_point = order.pickup_id.id
            if order.delivery_id:
                delivery_point = order.delivery_id.id
            if order.employee_id:
                employee_id = order.employee_id.id
            # Return order object
            res = {
                "id": order.id,
                "ship_code": order.ship_code,
                "date": order.date,
                "time_in": order.time_in,
                "payload": order.payload,
                "pickup_point": pickup_point,
                "delivery_point": delivery_point,
                "employee_id": employee_id,
            }
            data.append(res)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="get_orders_by_plan")
    def get_all_orders_in_transportation_plan(self, request, pk=None):
        qr_plan_id = request.data["plan_id"]
        query_data = Order.objects.filter(plan_id=qr_plan_id)
        data = []
        pickup_point = ""
        delivery_point = ""
        employee_id = ""
        for order in query_data:
            # Handle null data
            if order.pickup_id:
                pickup_point = order.pickup_id.id
            if order.delivery_id:
                delivery_point = order.delivery_id.id
            if order.employee_id:
                employee_id = order.employee_id.id
            # Return object
            res = {
                "id": order.id,
                "ship_code": order.ship_code,
                "date": order.date,
                "time_in": order.time_in,
                "payload": order.payload,
                "pickup_point": pickup_point,
                "delivery_point": delivery_point,
                "employee_id": employee_id,
            }
            data.append(res)
        return Response(data, status=status.HTTP_200_OK)
