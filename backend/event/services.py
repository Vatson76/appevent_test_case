import dateutil.parser
import logging

from hall.models import Hall
from .models import Event
from datetime import datetime

logger = logging.getLogger('backend.event.services')


def convert_json_to_datetime(string: str) -> datetime:
    return dateutil.parser.parse(string)


def delete_events_if_data_differs(hall: Hall, events: dict):
    logger.debug('Enter delete_events_if_data_differs function')

    hall_events = Event.objects.filter(hall=hall)
    if not hall_events.exists():
        logger.info('nothing to delete in database')
        return

    hall_db_events_ids_set = set(hall_events.values_list('google_id', flat=True))  # множество id событий в БД
    hall_calendar_events_ids_set = {event['id'] for event in events['items']}  # множество id событий из каленадя

    if hall_db_events_ids_set != hall_calendar_events_ids_set:  # если множества отличаются
        events_to_delete = Event.objects.filter(hall=hall).exclude(google_id__in=hall_calendar_events_ids_set)
        if events_to_delete.exists():
            events_to_delete_ids = events_to_delete.values_list('id', flat=True)
            logger.info('Deleted events with ids {}'.format(events_to_delete_ids))
            events_to_delete.delete()
        else:
            logger.info('Nothing to delete. Only new events in response')
    else:
        logger.info('Nothing to delete, data is valid')


def import_event(event: dict, hall):
    logger.info('Importing event with id {event_id} for hall {hall_name}'.format(
        event_id=event['id'],
        hall_name=hall.name
    ))

    date_start = event['start']['dateTime']
    date_end = event['end']['dateTime']

    filters = {
        'hall': hall,
        'google_id': event['id']
    }

    obj, created = Event.objects.update_or_create(
        **filters,
        defaults={
            'date_start': date_start,
            'date_end': date_end,
        }
    )
    if created:
        logger.info('Created new event with id {}'.format(
            obj.id
        ))
    else:
        logger.info('Updated event with id {}'.format(
            obj.id
        ))


def import_events(service, hall: Hall, import_time=None):
    """Импортирует события из Google calendar. Удаляет события, если данные в БД
     отличаются от данных в календаре"""
    logger.debug('Importing events import_time: {}'.format(import_time))

    events = service.events().list(calendarId=hall.google_calendar_id).execute()

    if import_time is not None:
        delete_events_if_data_differs(hall, events)
        event_list = [
            event for event in events['items'] if convert_json_to_datetime(event['created']) > import_time or
            (event.get('update') is not None and convert_json_to_datetime(event['update']) > import_time)
        ]
        for event in event_list:
            import_event(event, hall)
    else:
        delete_events_if_data_differs(hall, events)
        for event in events['items']:
            import_event(event, hall)
