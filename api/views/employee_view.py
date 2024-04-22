from .backend import *


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[
            permission_required("api.add_employee", raise_exception=False)
        ],
    )
    def create_user(self, request):
        data = request.data
        serializer_user = CreateEmployeeSerializer(data=data, many=True)
        if serializer_user.is_valid():
            serializer_user.create(serializer_user.validated_data)

            return Response("User is created!", status=status.HTTP_201_CREATED)
        return Response("User is not created!", status=status.HTTP_400_BAD_REQUEST)
