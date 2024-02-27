from api.models import HasNotification
from api.serializers import HasNotificationSerializer
from .backend import *


class HasNotificationViewSet(viewsets.ModelViewSet):
    queryset = HasNotification.objects.all()
    serializer_class = HasNotificationSerializer
    authentication_classes = (JWTAuthentication,)
