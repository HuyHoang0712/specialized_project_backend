from rest_framework import serializers
from api.models import *



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "date_time", "employess")