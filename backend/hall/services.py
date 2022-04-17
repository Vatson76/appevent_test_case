import logging

from .models import Hall

logger = logging.getLogger('backend.hall.services')


def import_calendars(service):
    logger.debug('Importing calendars'.format())

    calendar_list = service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
        Hall.objects.filter(
            name__icontains=calendar_list_entry['summary']
        ).update(google_calendar_id=calendar_list_entry['id'])
