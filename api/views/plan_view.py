from .backend import *
from datetime import datetime
import pandas as pd
import math
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser
from api.utils.distribute_order_service.main import distribute_orders

today = datetime.today().strftime("%Y-%m-%d")


class PlanViewSet(viewsets.ModelViewSet):
    queryset = TransportationPlan.objects.all()
    serializer_class = TransportationPlanSerializer
    authentication_classes = (JWTAuthentication,)

    # authentication_classes = ()
    # permission_classes = ()

    @action(detail=False, methods=["get"])
    def get_all_plans(self, request):
        queryset = TransportationPlan.objects.all()
        serializer = TransportationPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    @parser_classes([FileUploadParser])
    def file_upload(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = request.data["file"]
        reader = pd.read_excel(data, sheet_name=0, header=2)
        label_index = [0, 1, 4, 16]  # The column index in Excel file need to get data
        labels = ["ship_code", "contact_name", "order_type", "total_tons"]
        customers = []
        unknow_customers = set()
        plan_id = None
        for i in range(reader.shape[0]):
            customer = {
                label: (
                    reader.iloc[i, idx]
                    if idx != 16
                    else math.ceil(reader.iloc[i, idx] * 1000)
                )
                for label, idx in zip(labels, label_index)
            }
            queryset = Customer.objects.filter(
                name__unaccent__icontains=customer["contact_name"].strip()
            ).values()
            if queryset:
                item = queryset[0]
                customer["customer_id"] = item["id"]
                customer["longitude"] = item["longitude"]
                customer["latitude"] = item["latitude"]
                customers.append(customer)
            else:
                unknow_customers.add(customer["contact_name"])
        if unknow_customers:
            return Response(list(unknow_customers), status=status.HTTP_204_NO_CONTENT)
        else:
            # Call VRP algorithm
            plan_id = distribute_orders(customers)
        return (
            Response(plan_id, status=status.HTTP_200_OK)
            if plan_id
            else Response(
                {"detail": "No plan created"}, status=status.HTTP_204_NO_CONTENT
            )
        )
