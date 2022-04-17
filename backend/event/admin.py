from django.contrib import admin
from django.contrib.admin import display

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'hall', 'get_company', 'is_intersected')

    @display(ordering='hall__company__name', description='Компания')
    def get_company(self, obj):
        return obj.hall.company.name

    def is_intersected(self, obj):
        return obj.error

    is_intersected.short_description = 'Пересекается с другими событиями компании'
    is_intersected.boolean = True

