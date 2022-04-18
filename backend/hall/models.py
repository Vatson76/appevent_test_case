from django.db import models


class Hall(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название зала')
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        verbose_name='Компания',
        null=False,
        blank=False,
        related_name='hall'
    )
    google_calendar_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='id календаря google'
    )

    class Meta:
        ordering = 'name',
        verbose_name = 'Зал'
        verbose_name_plural = 'Залы'

    def __str__(self):
        return self.name
