from account.serializers.simulation import SimulationSerializer
from account.services.simulation import SimulationService
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class SimulationViewSet(viewsets.GenericViewSet):
    serializer_class = SimulationSerializer
    
    def list(self, request):
        pass