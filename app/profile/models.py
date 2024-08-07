import os
import uuid
from profile.enums import CategoryChoices, GenderChoices

from contact.enums import MessageStatus
from core.models import SoftDeletedModel, TimeStampModel
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


def profile_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "profile", filename)


class Profile(SoftDeletedModel, TimeStampModel):
    user = models.ForeignKey(
        get_user_model(), related_name="profiles", on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=200, null=True, unique=True)
    phone = models.CharField(
        max_length=15,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^(\+82|0)?1[0-9]{1}-?[0-9]{3,4}-?[0-9]{4}$",
                message="유효한 전화번호 형식이 아닙니다: 010-1234-5678 혹은 +82-10-1234-5678",
            )
        ],
    )
    gender = models.CharField(
        max_length=200, choices=GenderChoices.choices(), blank=True
    )
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=200, blank=True)
    residence = models.CharField(max_length=200, blank=True)
    religion = models.CharField(max_length=200, blank=True)
    is_smoke = models.BooleanField(blank=True, default=False)
    drinking_frequency = models.CharField(max_length=200, blank=True)

    @property
    def main_image(self):
        image = self.images.filter(is_main=True).first()
        return image

    def has_match(self, profile):
        sent_message = self.sent_message(profile)
        if sent_message:
            received_message = profile.sent_message(self)
            if received_message:
                return sent_message.filter(id__in=received_message).values_list(
                    "message_type__name", flat=True
                )

        return None

    def sent_message(self, profile):
        sent_message = self.messages.filter(receiver=profile).exclude(receiver=self)

        if sent_message.exists():
            return sent_message
        return None


class ProfileImage(SoftDeletedModel, TimeStampModel):
    profile = models.ForeignKey(
        "Profile", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(blank=True, null=True, upload_to=profile_image_file_path)
    is_main = models.BooleanField(default=False)


class Simulation(SoftDeletedModel, TimeStampModel):
    category = models.CharField(
        max_length=20, choices=CategoryChoices.choices(), blank=True
    )
    question = models.CharField(max_length=200, blank=True)


class AnswerChoice(models.Model):
    simulation = models.ForeignKey(
        "Simulation", related_name="answer_choices", on_delete=models.CASCADE
    )
    index = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["simulation", "index"],
                name="unique_simulation_index",
            )
        ]


class ProfileAnswer(SoftDeletedModel, TimeStampModel):
    profile = models.ForeignKey(
        "Profile", related_name="answers", on_delete=models.CASCADE
    )
    simulation = models.ForeignKey("Simulation", on_delete=models.CASCADE)
    answer_choice = models.ForeignKey("AnswerChoice", on_delete=models.CASCADE)

    @property
    def question(self):
        if self.simulation:
            return self.simulation.question
        return

    @property
    def answer(self):
        if self.answer_choice:
            return self.answer_choice.content
