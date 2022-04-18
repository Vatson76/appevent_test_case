import logging

from django.core.management.base import BaseCommand

from company.models import Company
from main.services import authorize_and_build_service
from hall.services import import_calendars

logger = logging.getLogger('backend.event.commands.import_events')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('company_id', nargs='?', type=int, default=None)

    def handle(self, *args, **options):
        logger.debug('Enter import_halls command with args: company_id: {company_id},'.format(
            company_id=options['company_id'],
        ))

        if options['company_id']:
            companies = Company.objects.filter(pk=options['company_id'])
        else:
            companies = Company.objects.all()

        for company in companies:
            service = authorize_and_build_service(company.id)
            import_calendars(service)
