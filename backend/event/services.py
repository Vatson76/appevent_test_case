from django.db.models import Q

from datetime import datetime

from hall.models import Hall
from .models import Event


def check_if_intersecting_events_exist(event_date_start: datetime, event_date_end: datetime, company_id: int) -> bool:
    """Проверяет, есть ли пересекающиеся события.
    Если есть, возвращает True и устанавливает им error=True.
    В противном случае возвращает False"""

    company_events = Event.objects.filter(hall__company_id=company_id)

    intersecting_events = company_events.filter(
        Q(Q(date_start__lt=event_date_start) & Q(date_end__gt=event_date_start)) |
        Q(Q(date_start__lt=event_date_end) & Q(date_end__gt=event_date_end))
    )
    if intersecting_events.exists():
        intersecting_events.update(error=True)
        return True
    else:
        return False


def import_event(event: dict, hall):
    date_start = event['start']['dateTime']
    date_end = event['end']['dateTime']

    filters = {
        'hall': hall,
        'date_start': date_start,
        'date_end': date_end
    }

    if check_if_intersecting_events_exist(date_start, date_end, hall.company_id):
        Event.objects.update_or_create(
            **filters,
            defaults={
                'google_id': event['id'],
                'error': True
            }
        )
    else:
        Event.objects.update_or_create(
            **filters,
            defaults={
                'google_id': event['id'],
            }
        )


def import_events(service, hall: Hall, import_time=None):
    events = service.events().list(calendarId=hall.google_calendar_id).execute()
    hall_events = Event.objects.filter(hall=hall)
    hall_bd_events_ids_list = hall_events.values_list('google_id', flat=True)
    hall_calendar_events_ids_list = [event['id'] for event in events['items']]

    if set(hall_bd_events_ids_list) != set(hall_calendar_events_ids_list):
        for event in events['items']:
            import_event(event, hall)
        Event.objects.filter(hall=hall).exclude(google_id__in=hall_calendar_events_ids_list).delete()
    elif import_time is None:
        for event in events['items']:
            import_event(event, hall)
    else:
        event_list = [event for event in events['items'] if event['created'] > import_time]
        for event in event_list:
            import_event(event, hall)
