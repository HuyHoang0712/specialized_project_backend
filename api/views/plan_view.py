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
        for i in range(0, reader.shape[0]):
            customer = {
                "ship_code": "",
                "contact_name": "",
                "longtitude": "",
                "latitude": "",
                "order_type": "",
                "total_tons": "",
            }
            count = 0
            for i1 in label_index:
                if count == 0:
                    customer["ship_code"] = reader.iloc[i, i1]
                elif count == 1:
                    customer["contact_name"] = reader.iloc[i, i1]
                elif count == 2:
                    customer["order_type"] = reader.iloc[i, i1]
                elif count == 3:
                    customer["total_tons"] = math.ceil(reader.iloc[i, i1] * 1000)
                count += 1
            qr_contact_name = customer["contact_name"]
            queryset = Customer.objects.filter(
                name__unaccent__icontains=qr_contact_name.strip()
            ).values()
            for item in queryset:
                if qr_contact_name.replace(" ", "") == item["name"].replace(" ", ""):
                    # print(True)
                    customer["longtitude"] = item["longitude"]
                    customer["latitude"] = item["latitude"]
                else:
                    unknow_customers.append(qr_contact_name)
            customers.append(customer)
        if len(unknow_customers) != 0:
            res = []
            [res.append(x) for x in unknow_customers if x not in res]
            return Response(res, status=status.HTTP_204_NO_CONTENT)
        return Response(customers, status=status.HTTP_200_OK)
