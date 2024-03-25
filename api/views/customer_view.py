from .backend import *
from api.utils.get_location_service.get_location import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def create_customer(self, request):
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

        print(data)
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
