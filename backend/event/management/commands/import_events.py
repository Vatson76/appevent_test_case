import argparse
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from event.services import import_events
from company.models import Company
from main.services import authorize_and_build_service

from datetime import timedelta

logger = logging.getLogger('backend.event.commands.import_events')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('company_id', nargs='?', type=int, default=None)
        parser.add_argument('--timed', action=argparse.BooleanOptionalAction, default=False)

    def handle(self, *args, **options):
        logger.debug('Enter import_events command with args: company_id: {company_id}, timed: {timed}'.format(
            company_id=options['company_id'],
            timed=options['timed']
        ))
        
        if options['timed']:
            import_time = timezone.now() - timedelta(minutes=2)
        else:
            import_time = None
        if options['company_id']:
            companies = Company.objects.filter(pk=options['company_id'])
        else:
            companies = Company.objects.all()

        for company in companies:
            service = authorize_and_build_service(company.id)
            for hall in company.hall.all():
                import_events(service, hall, import_time)
