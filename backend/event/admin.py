from django.contrib import admin
from django.contrib.admin import display

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'hall', 'get_company', 'intersects_with_other_events')

    @display(ordering='hall__company__name', description='Компания')
    def get_company(self, obj):
        return obj.hall.company.name

    def intersects_with_other_events(self, obj):
        return obj.intersects_with_other_events

    intersects_with_other_events.short_description = 'Пересекается с другими событиями компании'
    intersects_with_other_events.boolean = True

