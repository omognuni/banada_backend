from account.models import Simulation
from rest_framework import serializers


class SimulationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Simulation
        fields = ("id", "category", "question")
