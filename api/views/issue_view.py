from .backend import *
from datetime import datetime, timedelta


start = datetime.today().now().replace(hour=0, minute=0, second=0, microsecond=0)
end = datetime.today().now().replace(
    hour=0, minute=0, second=0, microsecond=0
) + timedelta(days=1, microseconds=-1)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by("-date_time").values()
    serializer_class = IssueSerializer
    authentication_classes = (JWTAuthentication,)

    @action(detail=False, methods=["post"])
    def get_issues_by_date(self, request, pk=None):
        qr_date = request.data["date"]
        queryset = Issue.objects.filter(date_time=qr_date)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
