from account.models import Simulation, Answer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Simulation.objects.create(question="나의 장단점은 무엇인가요?")
        Simulation.objects.create(question="나의 소확행은 무엇인가요?")
        Simulation.objects.create(question="성장을 위해 했던 경험과 앞으로의 계획을 적어주세요.")