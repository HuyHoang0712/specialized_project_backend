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

    @action(detail=False, methods=["get"])
    def get_vehicle_by_license(self, request):
        vehicle_license = request.query_params.get("license_plate")
        vehicle = Vehicle.objects.get(license_plate=vehicle_license)
        serializer = VehicleDetailSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def assign_driver(self, request):
        vehicle_license = request.data.get("license_plate")
        driver_id = request.data.get("driver_id")
        try:
            vehicle = Vehicle.objects.get(license_plate=vehicle_license)
            driver = Employee.objects.get(id=driver_id)

            vehicle.driver = driver
            vehicle.save()
            return Response({"message": "Driver assigned successfully"}, status=status.HTTP_200_OK)
        except not Vehicle:
            return Response({"error": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
        except not Employee:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

