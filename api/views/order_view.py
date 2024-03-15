from .backend import *
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # authentication_classes = (JWTAuthentication,)
    authentication_classes = ()
    permission_classes = ()

    @action(detail=False, methods=["get"])
    def get_orders_by_date(self, request, pk=None):
        qr_date = request.query_params["date"]
        queryset = Order.objects.filter(date=qr_date)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get_orders_in_plan")
    def get_all_orders_in_transportation_plan(self, request, pk=None):
        qr_plan = request.query_params["plan_id"]
        queryset = Order.objects.filter(plan=qr_plan)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="get_order_by_id")
    def get_order_by_id(self, request, pk=None):
        qr_id = request.query_params["id"]
        queryset = Order.objects.filter(id=qr_id)
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
    )
    def upldate_data(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OrderDetailSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
