from rest_framework import serializers
from api.models import *
import functools

class TransportationPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransportationPlan
        fields = ("id", "date")

    def to_representation(self, instance):
        orders = Order.objects.filter(plan__id=instance.id)
        total_order = orders.count()
        pending_order = orders.filter(status=0).count()
        completed_order = orders.filter(status=2).count()
        in_progress_order = orders.filter(status=1).count()
        cancel_order = orders.filter(status=3).count()
        issue_count = functools.reduce(lambda a, b: Issue.objects.filter(order__id=b.id).count() + a, orders, 0)

        return {
            "id": instance.id,
            "date": instance.date,
            "total_order": total_order,
            "pending_order": pending_order,
            "completed_order": completed_order,
            "in_progress_order": in_progress_order,
            "cancel_order": cancel_order,
            "issue_count": issue_count
        }