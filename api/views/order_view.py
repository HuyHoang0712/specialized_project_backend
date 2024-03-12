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

<<<<<<< Updated upstream
    @action(detail=False, methods=["post"])
    def get_orders_by_date(self, request, pk=None):
        qr_date = request.data["date"]
        query_data = Order.objects.filter(date=qr_date)
        data = []
        # count = 0
        for order in query_data:
            res = {
                "id": order.id,
                "ship_code": order.ship_code,
                "date": order.date,
                "time_in": order.time_in,
                "payload": order.payload,
                "pickup_point": order.pickup_id.name,
                "delivery_point": order.delivery_id.name,
                "employee_id": order.employee_id.id,
            }
            # data[count] = res
            # count += 1
=======
    @action(detail=False, methods=["GET"], url_path="get_orders_by_date")
    def get_orders_by_today(self, request, pk=None):
        q1 = Order.objects.filter(date=today)
        data = []
        for x in q1:
            res = {
                "id": x.id,
                "ship_code": x.ship_code,
                "date": x.date,
                "time_in": x.time_in,
                "payload": x.payload,
                "pickup_id": x.pickup_id.id,
                "employee_id": x.employee_id.id,
                "plan_id": x.plan_id.id,
            }
>>>>>>> Stashed changes
            data.append(res)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="get_orders_by_plan")
    def get_all_orders_in_transportation_plan(self, request, pk=None):
        body_unicode = request.body.decode("utf-8")
        body_data = json.loads(body_unicode)
        q1 = Order.objects.filter(plan_id=body_data["plan_id"])
        data = []
        for x in q1:
            res = {
                "id": x.id,
                "ship_code": x.ship_code,
                "date": x.date,
                "time_in": x.time_in,
                "payload": x.payload,
                "pickup_id": x.pickup_id.id,
                "employee_id": x.employee_id.id,
                "plan_id": x.plan_id.id,
            }
            data.append(res)
        return Response(data, status=status.HTTP_200_OK)
