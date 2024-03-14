from .backend import *
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")


class PlanViewSet(viewsets.ModelViewSet):
    queryset = TransportationPlan.objects.all()
    serializer_class = TransportationPlanSerializer
    # authentication_classes = (JWTAuthentication,)
    authentication_classes = ()
    permission_classes = ()

    @action(detail=False, methods=['get'])
    def get_all_plans(self, request):
        queryset = TransportationPlan.objects.all()
        serializer = TransportationPlanSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
