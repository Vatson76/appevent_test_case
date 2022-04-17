from django.db import models
from django.utils import timezone


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
    error = models.BooleanField(default=False, verbose_name='Пересекается с другими событиями компании?')

    class Meta:
        ordering = 'date_start',
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return '{hall_name} -- {date_start}'.format(
            hall_name=self.hall.name,
            date_start=timezone.localtime(self.date_start).strftime("%d.%m.%Y, %H:%M")
        )
