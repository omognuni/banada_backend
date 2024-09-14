from profile.models import AnswerChoice, Simulation

from rest_framework import serializers


class SimulationSerializer(serializers.ModelSerializer):
    answer_choices = serializers.SerializerMethodField()

    class Meta:
        model = Simulation
        fields = ("id", "category", "question", "answer_choices")

    def get_answer_choices(self, obj):
        return [choice.content for choice in obj.answer_choices.all()]
