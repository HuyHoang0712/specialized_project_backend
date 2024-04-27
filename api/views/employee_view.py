from .backend import *


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def create_user(self, request):
        data = request.data
        print(data)
        serializer_user = CreateEmployeeSerializer(data=data)
        if serializer_user.is_valid():
            serializer_user.create(serializer_user.validated_data)

            return Response("User is created!", status=status.HTTP_201_CREATED)
        return Response(serializer_user.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def get_employee_summary(self, request):
        data = Employee.objects.all()
        total = data.count()
        available = data.filter(status=0).count()
        busy = data.filter(status=1).count()
        on_break = data.filter(status=2).count()
        response = {
            "total": total,
            "available": available,
            "busy": busy,
            "on_break": on_break,
        }

        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_groups(self, request):
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


