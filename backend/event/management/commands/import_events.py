from django.core.management.base import BaseCommand
from decouple import config
from event.services import import_events
from company.models import Company
from hall.models import Hall
from main.services import authorize_and_build_service


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('company_id', nargs='?', type=int, default=None)

    def handle(self, *args, **options):
        if options['company_id']:
            companies = Company.objects.filter(pk=options['company_id'])
        else:
            companies = Company.objects.all()

        for company in companies:
            service = authorize_and_build_service(company.id)
            for hall in company.hall.all():
                import_events(service, hall)
