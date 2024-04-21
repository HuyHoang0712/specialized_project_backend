from .backend import *
from api.utils.get_location_service.get_location import *



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def create_customer(self, request):
        # Check permission
        if not request.user.has_perm("api.add_customer"):
            return Response("You don't have permission to create Customer", status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        print(data)
        if data["address"]:
            response = get_coordinate(data["address"])
            if response["status"] == "OK":
                coordinates = response["coordinate"]
                data["longitude"] = coordinates["lng"]
                data["latitude"] = coordinates["lat"]
            else:
                return Response(response["status"], status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Please input address", status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def get_customer_by_id(self, request):
        if not request.user.has_perm("api.view_customer"):
            return Response("You don't have permission to view Customer", status=status.HTTP_400_BAD_REQUEST)
        qr_id = request.query_params["id"]
        queryset = Customer.objects.get(id=qr_id)
        serializer = CustomerSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["put"])
    def update_customer(self, request):
        if not request.user.has_perm("api.change_customer"):
            return Response("You don't have permission to update Customer", status=status.HTTP_400_BAD_REQUEST)
        customer_id = request.query_params["id"]
        data = request.data
        if "address" in data.keys():
            response = get_coordinate(data["address"])
            if response["status"] == "OK":
                coordinates = response["coordinate"]
                data["longitude"] = coordinates["lng"]
                data["latitude"] = coordinates["lat"]
            else:
                return Response("Invalid Address!", status=status.HTTP_400_BAD_REQUEST)
        customer = Customer.objects.get(id=customer_id)
        if customer:
            serializer = CustomerSerializer(customer, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Customer is not founded!", status=status.HTTP_404_NOT_FOUND)