from django.contrib import admin
from .models import Hall


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
