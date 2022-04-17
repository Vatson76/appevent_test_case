from django.db import models
from django.utils import timezone
from django.db.models import Q


class Event(models.Model):
    hall = models.ForeignKey(
        'hall.Hall',
        on_delete=models.CASCADE,
        verbose_name='Зал',
        null=False,
        blank=False,
        related_name='event'
    )
    google_id = models.CharField(max_length=128, verbose_name='id события в календаре')
    date_start = models.DateTimeField(null=False, blank=False, verbose_name='Время начала события')
    date_end = models.DateTimeField(null=False, blank=False, verbose_name='Время окончания события')

    class Meta:
        ordering = 'date_start',
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return '{hall_name} -- {date_start}'.format(
            hall_name=self.hall.name,
            date_start=timezone.localtime(self.date_start).strftime("%d.%m.%Y, %H:%M")
        )

    @property
    def intersects_with_other_events(self):
        """Проверяет, есть ли пересекающиеся события"""

        company_events = Event.objects.filter(hall__company_id=self.hall.company_id)

        intersecting_events = company_events.filter(
            Q(Q(date_start__lt=self.date_start) & Q(date_end__gt=self.date_start)) |
            Q(Q(date_start__lt=self.date_end) & Q(date_end__gt=self.date_end))
        )
        if intersecting_events.exists():
            return True
        else:
            return False
