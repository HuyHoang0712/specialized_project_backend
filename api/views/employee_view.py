from .backend import *


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
    )

    @action(detail=False, methods=["post"])
    def create_user(self, request):
        data = request.data
        serializer_user = CreateEmployeeSerializer(data=data, many=True);
        if serializer_user.is_valid():
            serializer_user.create(serializer_user.validated_data)

            return Response("User is created!", status=status.HTTP_201_CREATED)
        return Response("User is not created!", status=status.HTTP_400_BAD_REQUEST)

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
