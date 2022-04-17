from django.utils import timezone

from hall.models import Hall
from .models import Event
from datetime import datetime
import dateutil.parser


def convert_json_to_datetime(string: str) -> datetime:
    return dateutil.parser.parse(string)


def delete_events_if_data_differs(hall: Hall, events: dict):
    hall_events = Event.objects.filter(hall=hall)
    if not hall_events.exists():
        return

    hall_db_events_ids_set = set(hall_events.values_list('google_id', flat=True))  # множество id событий в БД
    hall_calendar_events_ids_set = {event['id'] for event in events['items']}  # множество id событий из каленадя

    if hall_db_events_ids_set != hall_calendar_events_ids_set:  # если множества отличаются
        Event.objects.filter(hall=hall).exclude(google_id__in=hall_calendar_events_ids_set).delete()


def import_event(event: dict, hall):
    date_start = event['start']['dateTime']
    date_end = event['end']['dateTime']

    filters = {
        'hall': hall,
        'google_id': event['id']
    }

    Event.objects.update_or_create(
        **filters,
        defaults={
            'date_start': date_start,
            'date_end': date_end,
        }
    )


def import_events(service, hall: Hall, import_time=None):
    """Импортирует события из Google calendar. Удаляет события, если данные в БД
     отличаются от данных в календаре"""
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
        for event in events['items']:
            delete_events_if_data_differs(hall, events)
            import_event(event, hall)
