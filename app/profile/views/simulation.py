from profile.models import Simulation
from profile.serializers.simulation import (
    SimulationPatchSerializer,
    SimulationSerializer,
)

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets


@extend_schema(tags=["Simulation"])
class SimulationViewSet(viewsets.ModelViewSet):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer

    def create(self, request, *args, **kwargs):
        """
        Index - 답변이 나열 되는 순서
        Content - 답변 내용
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(request=SimulationPatchSerializer, tags=["Simulation"])
    def partial_update(self, request, *args, **kwargs):
        """
        id - 변경할 답변(AnswerChoice)의 ID
        index - 답변이 나열 되는 순서
        content - 답변 내용
        """
        return super().partial_update(request, *args, **kwargs)()
