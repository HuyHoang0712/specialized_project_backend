from api.models import Vehicle
from api.serializers import VehicleSerializer
from .backend import *


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_vehicle", raise_exception=True),
        permission_required("api.add_vehicle", raise_exception=True),
        permission_required("api.change_vehicle", raise_exception=True),
        permission_required("api.delete_vehicle", raise_exception=True),
    )
