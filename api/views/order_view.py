from .backend import *
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

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
        queryset = Order.objects.get(id=qr_id)
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
        qr_id = request.query_params["id"]
        order = Order.objects.get(id=qr_id)
        if order:
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res_serializer = OrderDetailSerializer(order)
                return Response(res_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Order is not founded!", status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def get_recent_orders_coordinates(self, request, pk=None):
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
