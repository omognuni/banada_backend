from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(10):
            get_user_model().objects.create_user(
                username=f"test{i}", password="testpass"
            )
