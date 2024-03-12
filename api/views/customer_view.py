from .backend import *


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (
        IsAuthenticated,
    )
