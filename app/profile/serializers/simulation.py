from profile.models import AnswerChoice, Simulation

from rest_framework import serializers


class SimulationAnswerChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerChoice
        fields = ("id", "simulation", "index", "content")


class SimulationSerializer(serializers.ModelSerializer):
    answer_choices = SimulationAnswerChoiceSerializer(many=True)

    class Meta:
        model = Simulation
        fields = ("id", "category", "question", "answer_choices")
