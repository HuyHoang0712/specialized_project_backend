from api.models import Issue
from api.serializers import IssueSerializer
from .backend import *
from datetime import datetime, timedelta


start = datetime.today().now().replace(hour=0, minute=0, second=0, microsecond=0)
end = datetime.today().now().replace(
    hour=0, minute=0, second=0, microsecond=0
) + timedelta(days=1, microseconds=-1)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    authentication_classes = (JWTAuthentication,)

    @action(detail=False, methods=["GET"])
    def get_issues_by_today(self, request, pk=None):
        issues = Issue.objects.filter(date_time__range=(start, end))
        creator_id = ""
        order_id = ""
        vehicle_license_plate = ""
        warehouse_id = ""
        data = []
        for issue in issues:
            # Handle null data
            if issue.creator_id:
                creator_id = issue.creator_id.id
            if issue.order_id:
                order_id = issue.order_id.id
            if issue.vehicle_license_plate:
                vehicle_license_plate = issue.vehicle_license_plate.license_plate
            if issue.warehouse_id:
                warehouse_id = issue.warehouse_id.id
            # Return issue object
            res = {
                "title": issue.title,
                "description": issue.description,
                "date_time": issue.date_time,
                "status": issue.status,
                "label": issue.label,
                "creator_id": creator_id,
                "order_id": order_id,
                "vehicle_license_plate": vehicle_license_plate,
                "warehouse_id": warehouse_id,
            }
            data.append(res)
        return Response(data, status=status.HTTP_200_OK)
