from api.models import Issue
from api.serializers import IssueSerializer
from .backend import *


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    authentication_classes = (JWTAuthentication,)
