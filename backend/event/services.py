from hall.models import Hall
from .models import Event


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
    """Импортирует события из Google calendar.
    Вычисляет, какие события нужно импортировать при помощи разности множеств событий,
    представленных в бд и событий в календаре.
    Если """
    events = service.events().list(calendarId=hall.google_calendar_id).execute()
    hall_events = Event.objects.filter(hall=hall)

    hall_db_events_ids_set = set(hall_events.values_list('google_id', flat=True))  # множество id событий в БД
    hall_calendar_events_ids_set = {event['id'] for event in events['items']}  # множество id событий из каленадя

    hall_calendar_events_ids_dict = {event['id']: event for event in events['items']}  # делаем dict, чтобы потом
    # не тратить время на поиски нужных событий

    if import_time is not None:
        event_list = [
            event for event in events['items']
            if event['created'] > import_time or event['update'] > import_time
        ]
        for event in event_list:
            import_event(event, hall)
    elif hall_db_events_ids_set != hall_calendar_events_ids_set:  # если множества отличаются
        what_elements_to_import = hall_calendar_events_ids_set - hall_db_events_ids_set  # ищем, какие события нужно
        # импортировать путем вычитания множеств
        for event_id in what_elements_to_import:
            import_event(hall_calendar_events_ids_dict[event_id], hall)
        Event.objects.filter(hall=hall).exclude(google_id__in=hall_calendar_events_ids_set).delete()
    elif import_time is None:
        for event in events['items']:
            import_event(event, hall)
