from .backend import *
from datetime import datetime
import pandas as pd
import math

today = datetime.today().strftime("%Y-%m-%d")


class PlanViewSet(viewsets.ModelViewSet):
    queryset = TransportationPlan.objects.all()
    serializer_class = TransportationPlanSerializer
    # authentication_classes = (JWTAuthentication,)
    authentication_classes = ()
    permission_classes = ()

    @action(detail=False, methods=["get"])
    def get_all_plans(self, request):
        queryset = TransportationPlan.objects.all()
        serializer = TransportationPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def file_upload(self, request):
        data = None
        if request.method == "POST":
            data = request.FILES["file_upload"]
            reader = pd.read_excel(
                data,
                sheet_name=0,
                header=2,
            )
            print(reader.shape[0])
            # print(reader.loc[0])
            customers = []
            label_index = [0, 1, 4, 16]
            for i in range(0, reader.shape[0]):
                customer = {
                    "ship_code": "",
                    "contact_name": "",
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
                customers.append(customer)
            print(customers)

        return Response(customers, status=status.HTTP_200_OK)
