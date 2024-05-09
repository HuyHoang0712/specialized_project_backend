from django.contrib.auth import authenticate

from .backend import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SupervisorLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if user:

                if not user.has_perm("api.supervisor"):
                    return Response(
                        {"error_message": "Permission Required!", "error_code": 403},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                token = TokenObtainPairSerializer.get_token(user)
                data = {
                    "refresh_token": str(token),
                    "access_token": str(token.access_token),
                    "access_expires": int(
                        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                    ),
                    "refresh_expires": int(
                        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
                    ),
                    "user_name": user.first_name + " " + user.last_name,
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"error_message": "Email or password is incorrect!", "error_code": 400},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"error_messages": serializer.errors, "error_code": 400},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EmployeeLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request: Request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if user:
                token = TokenObtainPairSerializer.get_token(user)
                data = {
                    "refresh_token": str(token),
                    "access_token": str(token.access_token),
                    "access_expires": int(
                        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
                    ),
                    "refresh_expires": int(
                        settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
                    ),
                    "user_name": user.first_name + " " + user.last_name,
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"error_message": "Email or password is incorrect!", "error_code": 400},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"error_messages": serializer.errors, "error_code": 400},
            status=status.HTTP_400_BAD_REQUEST,
        )