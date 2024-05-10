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

    @action(detail=False, methods=["get"])
    def get_issues_by_employee_id(self, request, pk=None):
        qr_employee_id = request.query_params["employee_id"]
        queryset = Issue.objects.filter(creator=qr_employee_id).order_by("-date_time")
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_issues_of_vehicle(self, request, pk=None):
        qr_vehicle_id = request.query_params["vehicle"]
        queryset = Issue.objects.filter(issuevehicle__vehicle_id=qr_vehicle_id)
        serializer = VehicleIssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_issues(self, request, pk=None):
        qr_type = request.query_params["type"]
        flag = "status" in request.query_params

        if qr_type == "issue-vehicle":
            queryset = Issue.objects.filter(status=request.query_params["status"],
                                            issuevehicle__isnull=False) if flag else Issue.objects.filter(
                issuevehicle__isnull=False)
            serializer = VehicleIssueSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = Issue.objects.filter(status=request.query_params["status"],
                                        issuevehicle__isnull=True) if flag else Issue.objects.filter(
            issuevehicle__isnull=True)
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_issue_by_id(self, request, pk=None):
        qr_id = request.query_params["id"]
        queryset = Issue.objects.get(id=qr_id)
        if IssueVehicle.objects.filter(request_id=qr_id).exists():
            serializer = VehicleIssueSerializer(queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = IssueSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_user_issues(self, request, pk=None):
        account_id = request.user.id
        profile = Employee.objects.filter(user=account_id)
        serializer = EmployeeSerializer(profile, many=True)
        employee_id = serializer.data[0]["id"]
        employee_issue = Issue.objects.filter(creator=employee_id)
        return_issues = IssueSerializer(employee_issue, many=True)
        return Response(return_issues.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"])
    def update_issue_status(self, request, pk=None):
        qr_id = request.query_params["id"]
        qr_type = request.query_params["type"]

        issue = Issue.objects.get(id=qr_id)
        if qr_type == "issue-vehicle":
            serializers = VehicleIssueSerializer(issue, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        serializers = IssueSerializer(issue, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_200_OK)


    @action(detail=False, methods=["post"])
    def create_issue(self, request):
        data = request.data
        rq_type = request.query_params["type"]
        data["creator"] = Employee.objects.get(user__id=data["creator"]).id
        if rq_type == "vehicle":
            serializer_issue = VehicleIssueSerializer(data=data)
            if serializer_issue.is_valid():
                new_issue = serializer_issue.create(serializer_issue.validated_data, data["vehicle_id"], data["cost"])
                return Response(new_issue, status=status.HTTP_201_CREATED)
            return Response(serializer_issue.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer_issue = IssueSerializer(data=data)
        if serializer_issue.is_valid():
            serializer_issue.save()
            return Response(serializer_issue.data, status=status.HTTP_201_CREATED)
        return Response(serializer_issue.errors, status=status.HTTP_400_BAD_REQUEST)
