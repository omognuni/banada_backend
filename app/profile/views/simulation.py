from profile.models import Simulation
from profile.serializers.simulation import SimulationSerializer

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets


@extend_schema(tags=["Simulation"])
class SimulationViewSet(viewsets.ModelViewSet):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
