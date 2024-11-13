from tkinter.constants import CASCADE

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}

class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Создатель привычки')
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', related_name='retalted_to', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Связанная привычка')
    periodicity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(7)], verbose_name='Периодичность')
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name='Награда')
    duration = models.DurationField(verbose_name='Время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичной привычки')

    class Meta:
        verbose_name = 'Привычка',
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'Привычка пользователя {self.owner} - я буду {self.action} в {self.time} в {self.place}'
