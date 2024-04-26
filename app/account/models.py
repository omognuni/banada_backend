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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    height = models.IntegerField(blank=True, null=True)
    job = models.CharField(max_length=20, blank=True)
    residence = models.CharField(max_length=200, blank=True)


class Lifestyle(models.Model):
    religion = models.CharField(max_length=20, blank=True)
    is_smoke = models.BooleanField(default=False)
    drinking_frequency = models.CharField(max_length=20, blank=True)


class Image(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=profile_image_file_path)


class AnswerHistory(models.Model):
    question = models.ForeignKey(
        "Question", related_name="histories", on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        "Profile", related_name="answers", on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        "Answer", related_name="questions", on_delete=models.CASCADE
    )


class Question(models.Model):
    category = models.CharField(max_length=20, blank=True)
    question = models.CharField(max_length=200, blank=True)


class Answer(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.CharField(max_length=200, blank=True)
