from .models import Hall


def import_calendars(service):
    calendar_list = service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
        Hall.objects.filter(
            name__icontains=calendar_list_entry['summary']
        ).update(google_calendar_id=calendar_list_entry['id'])
