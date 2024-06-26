from .backend import *
from ..utils.notification_service import notification


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def create_user(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = request.data
        serializer_user = CreateEmployeeSerializer(data=data)
        if serializer_user.is_valid():
            serializer_user.create(serializer_user.validated_data)
            serializer_data = serializer_user.data
            notification.send_welcome_email(
                serializer_data["username"],
                serializer_data["password"],
                serializer_data["email"],
            )
            return Response("User is created!", status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Username or Email already exists. Please try again!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=["get"])
    def get_employee_summary(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = Employee.objects.all()
        total = data.count()
        available = data.filter(status=2).count()
        busy = data.filter(status=1).count()
        on_break = data.filter(status=3).count()
        response = {
            "total": total,
            "available": available,
            "busy": busy,
            "on_break": on_break,
        }

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_groups(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_employee_by_id(self, request):
        employee_id = request.query_params.get("id")
        employee = Employee.objects.get(id=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["put"])
    def update_employee(self, request):
        data = request.data
        employee_id = request.query_params["id"]
        employee = Employee.objects.get(id=employee_id)
        serializer = UpdateEmployeeSerializer(data=data)
        if serializer.is_valid():
            employee = serializer.update(employee, serializer.validated_data)
            return Response(employee, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Employee information is invalid! Please try again!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, methods=["get"])
    def get_unassigned_employees(self, request):
        if not request.user.has_perm("api.supervisor"):
            return Response(
                {"error_message": "Permission Required!", "error_code": 403},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Get the 'employee' group
        employee_group = Group.objects.get(name="Driver")

        # Filter the employees who are in the 'employee' group and have not been assigned a vehicle
        unassigned_employees = Employee.objects.filter(
            user__groups=employee_group, vehicle__isnull=True
        )

        # Serialize the employees
        serializer = EmployeeSerializer(unassigned_employees, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["get"])
    def get_user_profile(self, request, pk=None):
        account_id = request.user.id

        profile = Employee.objects.filter(user=account_id)
        serializer = EmployeeSerializer(profile, many=True)
        return_data = serializer.data[0]
        return Response(return_data, status=status.HTTP_200_OK)
