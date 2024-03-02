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
        print(end)
        q1 = Issue.objects.filter(date_time__range=(start, end))
        data = {}
        count = 0
        for x in q1:
            res = {
                "title": x.title,
                "description": x.description,
                "date_time": x.date_time,
                "status": x.status,
                "label": x.label,
                "creator_id": x.creator_id,
                "order_id": x.order_id,
                "vehicle_license_plate": x.vehicle_license_plate,
                "warehouse_id": x.warehouse_id,
            }
            data[count] = res
            count += 1
        return Response(data, status=status.HTTP_200_OK)
