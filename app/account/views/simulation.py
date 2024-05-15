from account.models import Simulation
from account.serializers.simulation import SimulationSerializer
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets


@extend_schema(tags=["Simulation"])
class SimulationViewSet(viewsets.ModelViewSet):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
