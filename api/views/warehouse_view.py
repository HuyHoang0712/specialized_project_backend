from api.models import Warehouse
from api.serializers import WarehouseSerializer
from .backend import *


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_warehouse", raise_exception=True),
        permission_required("api.add_warehouse", raise_exception=True),
        permission_required("api.change_warehouse", raise_exception=True),
        permission_required("api.delete_warehouse", raise_exception=True),
    )

    def get_queryset(self):
        return Warehouse.objects.all()
