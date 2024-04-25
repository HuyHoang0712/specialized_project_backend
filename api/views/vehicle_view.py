from .backend import *


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
    )

    @action(detail=False, methods=["get"])
    def get_vehicle_brands(self, request):
        brands = Vehicle.objects.values("brand").distinct()
        return Response(brands, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def create_vehicle(self, request):
        data = request.data
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)