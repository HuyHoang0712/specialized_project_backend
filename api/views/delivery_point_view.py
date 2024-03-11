from api.models import DeliveryPoint
from api.serializers import DeliveryPointSerializer
from .backend import *


class DeliveryPointViewSet(viewsets.ModelViewSet):
    queryset = DeliveryPoint.objects.all()
    serializer_class = DeliveryPointSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_deliverypoint", raise_exception=True),
        permission_required("api.add_deliverypoint", raise_exception=True),
        permission_required("api.change_deliverypoint", raise_exception=True),
        permission_required("api.delete_deliverypoint", raise_exception=True),
    )
