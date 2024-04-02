from .backend import *
from datetime import datetime, timedelta


start = datetime.today().now().replace(hour=0, minute=0, second=0, microsecond=0)
end = datetime.today().now().replace(
    hour=0, minute=0, second=0, microsecond=0
) + timedelta(days=1, microseconds=-1)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by("-date_time")
    serializer_class = IssueSerializer
    authentication_classes = (JWTAuthentication,)

    @action(detail=False, methods=["post"])
    def get_issues_by_date(self, request, pk=None):
        qr_date = request.data["date"]
        queryset = Issue.objects.filter(date_time=qr_date)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_issues_by_status(self, request, pk=None):
        qr_status = request.query_params["status"]
        queryset = Issue.objects.filter(status=qr_status).order_by("-date_time")
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_user_issues(self, request, pk=None):
        account_id = request.user.id
        print(request.user.id)
        profile = Employee.objects.filter(user=account_id)
        profile_serializer = EmployeeSerializer(profile, many=True)
        employee_id = profile_serializer.data[0]["id"]
        print(profile_serializer.data[0]["id"])
        issues = Issue.objects.filter(creator=employee_id)
        issue_serializer = IssueSerializer(issues, many=True)
        return Response(issue_serializer.data, status=status.HTTP_200_OK)
