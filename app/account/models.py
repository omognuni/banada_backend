import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models


def profile_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "profile", filename)


class Profile(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="profiles", on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=20, blank=True)
    height = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=20, blank=True)
    residence = models.CharField(max_length=200, blank=True)
    religion = models.CharField(max_length=20, blank=True)
    is_smoke = models.BooleanField(blank=True, default=False)
    drinking_frequency = models.CharField(max_length=20, blank=True)


class ProfileImage(models.Model):
    profile = models.ForeignKey(
        "Profile", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(blank=True, null=True, upload_to=profile_image_file_path)


class Simulation(models.Model):
    category = models.CharField(max_length=20, blank=True)
    question = models.CharField(max_length=200, blank=True)


class Answer(models.Model):
    profile = models.ForeignKey(
        "Profile", related_name="answers", on_delete=models.CASCADE
    )
    simulation = models.ForeignKey(
        "Simulation", related_name="answers", on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=200, blank=True)

    @property
    def question(self):
        if self.simulation:
            return self.simulation.question
        return
