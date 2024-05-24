from .backend import *


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = (JWTAuthentication,)

    @action(detail=False, methods=["get"])
    def get_notifications(self, request):
        user_id = request.user.id
        employee = Employee.objects.get(user=user_id)
        notifications = HasNotification.objects.filter(employee=employee).order_by("-notification__send_datetime")
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"])
    def mark_as_read(self, request):
        notification_id = request.query_params["id"]
        user_id = request.user.id
        employee = Employee.objects.get(user=user_id)
        notification = HasNotification.objects.get(notification__id=notification_id, employee=employee)
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read!"}, status=status.HTTP_200_OK)
