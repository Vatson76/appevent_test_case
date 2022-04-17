from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название компании')

    class Meta:
        ordering = 'name',
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name
