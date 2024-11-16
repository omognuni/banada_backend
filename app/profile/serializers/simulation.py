from profile.models import AnswerChoice, Simulation

from rest_framework import serializers


class AnswerChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = AnswerChoice
        fields = ["id", "index", "content"]


class AnswerChoicePatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = AnswerChoice
        fields = ["id", "index", "content"]


class SimulationSerializer(serializers.ModelSerializer):
    answer_choices = AnswerChoiceSerializer(many=True, required=False)

    class Meta:
        model = Simulation
        fields = ("id", "category", "question", "answer_choices")

    def create(self, validated_data):
        answer_choices_data = validated_data.pop("answer_choices", [])
        simulation = Simulation.objects.create(**validated_data)
        for answer_choice_data in answer_choices_data:
            AnswerChoice.objects.create(simulation=simulation, **answer_choice_data)
        return simulation


class SimulationPatchSerializer(serializers.ModelSerializer):
    answer_choices = AnswerChoicePatchSerializer(many=True, required=False)

    class Meta:
        model = Simulation
        fields = ("id", "category", "question", "answer_choices")

    def update(self, instance, validated_data):
        answer_choices_data = validated_data.pop("answer_choices", [])
        instance.category = validated_data.get("category", instance.category)
        instance.question = validated_data.get("question", instance.question)
        instance.save()

        for answer_choice_data in answer_choices_data:
            answer_choice_id = answer_choice_data.get("id")
            if answer_choice_id:
                answer_choice = AnswerChoice.objects.get(
                    id=answer_choice_id, simulation=instance
                )
                answer_choice.index = answer_choice_data.get(
                    "index", answer_choice.index
                )
                answer_choice.content = answer_choice_data.get(
                    "content", answer_choice.content
                )
                answer_choice.save()
            else:
                AnswerChoice.objects.create(simulation=instance, **answer_choice_data)

        return instance
