from .backend import *


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = (JWTAuthentication,)
