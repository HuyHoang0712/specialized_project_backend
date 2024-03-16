from .backend import *
from datetime import datetime
import pandas as pd
import math
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FileUploadParser

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
        data = request.data["file"]
        reader = pd.read_excel(data, sheet_name=0, header=2)
        label_index = [0, 1, 4, 16]
        labels = ["ship_code", "contact_name", "order_type", "total_tons"]
        customers = []
        unknow_customers = set()

        for i in range(reader.shape[0]):
            customer = {label: reader.iloc[i, idx] if idx != 16 else math.ceil(reader.iloc[i, idx] * 1000) for
                        label, idx in zip(labels, label_index)}
            queryset = Customer.objects.filter(name__unaccent__icontains=customer["contact_name"].strip()).values()
            if queryset:
                unknow_customers.add(customer["contact_name"].strip())
            else:
                customers.append(customer)

        if unknow_customers:
            return Response(list(unknow_customers), status=status.HTTP_204_NO_CONTENT)
        return Response(customers, status=status.HTTP_200_OK)
