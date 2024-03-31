from .backend import *


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
        permission_required("api.view_employee", raise_exception=True),
        permission_required("api.add_employee", raise_exception=True),
        permission_required("api.change_employee", raise_exception=True),
        permission_required("api.delete_employee", raise_exception=True),
    )

    def get_queryset(self):
        return Employee.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["get"])
    def get_user_profile(self, request, pk=None):
        account_id = request.user.id
        print(request.user.id)
        profile = Employee.objects.filter(user=account_id)
        serializer = EmployeeSerializer(profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
