import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command

from company.models import Company
from hall.models import Hall

logger = logging.getLogger('backend.company.commands.populate_db_data')


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.debug('Enter populate_db_data')

        company1 = Company.objects.create(name='')
        company2 = Company.objects.create(name='')

        halls = (
            Hall(
                name='',
                company=company1,
                google_calendar_id='',
            ),
            Hall(
                name='',
                company=company2,
                google_calendar_id='',
            ),
            Hall(
                name='',
                company=company2,
                google_calendar_id='',
            ),
            Hall(
                name='',
                company=company2,
                google_calendar_id='',
            ),
            Hall(
                name='',
                company=company2,
                google_calendar_id='',
            )
        )
        Hall.objects.bulk_create(
            halls,
            batch_size=10,
            ignore_conflicts=True
        )
        #call_command('import_halls', verbosity=0)  # Расскоментируйте в случае необходимости импорта id залов

        call_command('import_events', verbosity=0)

        logger.info('Data populated')
