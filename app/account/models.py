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
    nickname = models.CharField()
    height = models.IntegerField()
    job = models.CharField()
    residence = models.CharField()


class Lifestyle(models.Model):
    religion = models.CharField()
    is_smoke = models.BooleanField(default=False)
    drinking_frequency = models.CharField()


class Image(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=profile_image_file_path)


class AnswerHistory(models.Model):
    question = models.ForeignKey("Question")
    profile = models.ForeignKey("Profile")
    answer = models.ForeignKey("Answer")


class Question(models.Model):
    category = models.CharField()
    question = models.CharField()


class Answer(models.Model):
    question = models.ForeignKey("Question")
    answer = models.CharField()
