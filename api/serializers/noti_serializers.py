from rest_framework import serializers
from api.models import *


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HasNotification
        fields = "__all__"

    def to_representation(self, instance):
        notification = instance.notification
        return_data = {
            "id": notification.id,
            "type": notification.type,
            "sender_id": notification.sender_id.id,
            "description": notification.description,
            "send_datetime": notification.send_datetime,
            "is_read": instance.is_read
        }
        if notification.type == 1:
            order = NotificationOrder.objects.get(notification=notification).order
            return_data["order_id"] = order.id
        elif notification.type == 2:
            issue = NotificationIssue.objects.get(notification=notification).issue
            return_data["issue_id"] = issue.id
        return return_data


class CreateNotificationSerializer(serializers.ModelSerializer):
    receiver_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all(), required=False)

    class Meta:
        model = Notification
        fields = ['type', 'sender_id', 'description', 'receiver_ids', 'order', 'issue']

    def create(self, validated_data):
        receiver_ids = validated_data.pop('receiver_ids')
        notification = Notification.objects.create(
            type=validated_data['type'],
            sender_id=validated_data['sender_id'],
            description=validated_data['description']
        )
        if validated_data['type'] == 1:
            notification_order = NotificationOrder.objects.create(
                notification=notification,
                order=validated_data['order']
            )
            notification_order.save()
        elif validated_data['type'] == 2:
            notification_issue = NotificationIssue.objects.create(
                notification=notification,
                issue=validated_data['issue']
            )
            notification_issue.save()
        notification.save()
        for receiver_id in receiver_ids:
            try:
                employee = Employee.objects.get(id=receiver_id)
                has_notification = HasNotification.objects.create(notification=notification, employee=employee)
                has_notification.save()
            except Employee.DoesNotExist:
                pass

        return notification

    def validate(self, data):
        if data['type'] == 1 and 'order' not in data:
            raise serializers.ValidationError("Order is required when type is 1")
        if data['type'] == 2 and 'issue' not in data:
            raise serializers.ValidationError("Issue is required when type is 2")
        return data
