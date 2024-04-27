from rest_framework import serializers
from account.models import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Simulation