from api.models import Order
from api.serializers import OrderSerializer
from .backend import *
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # authentication_classes = (JWTAuthentication,)
    authentication_classes = ()
    permission_classes = ()

    @action(detail=False, methods=["GET"])
    def get_orders_by_today(self, request, pk=None):
        q1 = Order.objects.filter(date=today)
        data = {}
        count = 0
        for x in q1:
            res = {
                "id": x.id,
                "ship_code": x.ship_code,
                "date": x.date,
                "time_in": x.time_in,
                "payload": x.payload,
                "pickup_id": x.pickup_id,
                "employee_id": x.employee_id,
            }
            data[count] = res
            count += 1
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_all_orders_in_transportation_plan(self, request, pk=None):
        q1 = Order.objects.filter(date=today)
        data = {}
        count = 0
        for x in q1:
            res = {
                "id": x.id,
                "ship_code": x.ship_code,
                "date": x.date,
                "time_in": x.time_in,
                "payload": x.payload,
                "pickup_id": x.pickup_id,
                "employee_id": x.employee_id,
            }
            data[count] = res
            count += 1
        return Response(data, status=status.HTTP_200_OK)
