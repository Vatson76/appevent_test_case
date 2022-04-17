from django.core.management.base import BaseCommand
from decouple import config


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
