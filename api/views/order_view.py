from .backend import *
from datetime import datetime

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
        queryset = Order.objects.filter(date=qr_date)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="get_orders_by_plan")
    def get_all_orders_in_transportation_plan(self, request, pk=None):
        qr_plan = request.data["plan"]
        queryset = Order.objects.filter(plan=qr_plan)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
