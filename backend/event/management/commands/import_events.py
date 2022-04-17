from django.core.management.base import BaseCommand
from decouple import config
from event.services import import_events
from hall.models import Hall
from main.services import authorize_and_build_service


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('company_id', nargs='?', type=int, default=None)

    def handle(self, *args, **options):
        if options['company_id']:
            halls = Hall.objects.filter(company_id=options['company_id'])
        else:
            halls = Hall.objects.all()
        service = authorize_and_build_service()

        for hall in halls:
            import_events(service, hall)
