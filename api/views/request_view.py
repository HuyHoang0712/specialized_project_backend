from .backend import *
from datetime import datetime, timedelta


start = datetime.today().now().replace(hour=0, minute=0, second=0, microsecond=0)
end = datetime.today().now().replace(
    hour=0, minute=0, second=0, microsecond=0
) + timedelta(days=1, microseconds=-1)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Requests.objects.all().order_by("-date_time")
    serializer_class = RequestSerializer
    authentication_classes = (JWTAuthentication,)

    @action(detail=False, methods=["post"])
    def get_requests_by_date(self, request, pk=None):
        qr_date = request.data["date"]
        queryset = Request.objects.filter(date_time=qr_date)
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_requests_by_status(self, request, pk=None):
        qr_status = request.query_params["status"]
        queryset = Request.objects.filter(status=qr_status).order_by("-date_time")
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_user_requests(self, request, pk=None):
        account_id = request.user.id
        print(request.user.id)
        profile = Employee.objects.filter(user=account_id)
        profile_serializer = EmployeeSerializer(profile, many=True)
        employee_id = profile_serializer.data[0]["id"]
        print(profile_serializer.data[0]["id"])
        requests = Request.objects.filter(creator=employee_id)
        issue_serializer = RequestSerializer(requests, many=True)
        return Response(issue_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_user_requests(self, request, pk=None):
        account_id = request.user.id
        print(request.user.id)
        profile = Employee.objects.filter(user=account_id)
        profile_serializer = EmployeeSerializer(profile, many=True)
        employee_id = profile_serializer.data[0]["id"]
        print(profile_serializer.data[0]["id"])
        requests = Request.objects.filter(creator=employee_id)
        issue_serializer = RequestSerializer(requests, many=True)
        return Response(issue_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_requests_by_employee_id(self, request, pk=None):
        qr_employee_id = request.query_params["employee_id"]
        queryset = Request.objects.filter(creator=qr_employee_id).order_by("-date_time")
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_requests_by_employee_id(self, request, pk=None):
        qr_employee_id = request.query_params["employee_id"]
        queryset = Request.objects.filter(creator=qr_employee_id).order_by("-date_time")
        serializer = RequestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)