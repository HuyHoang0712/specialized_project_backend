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
