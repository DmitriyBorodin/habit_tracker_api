# from multiselectfield import MultiSelectField

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Weekday(models.Model):
    day = models.CharField(max_length=20, verbose_name="День недели")
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        unique=True,
        verbose_name="Порядковый номер дня в неделе",
    )

    class Meta:
        verbose_name = ("День недели",)
        verbose_name_plural = "Дни недели"

    def __str__(self):
        return self.day


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Создатель привычки",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        related_name="retalted_to",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Связанная привычка",
    )
    # periodicity = models.PositiveIntegerField(default=1,
    #                                           validators=[MinValueValidator(1),
    #                                                       MaxValueValidator(7)],
    #                                           verbose_name='Периодичность')
    weekdays = models.ManyToManyField(
        Weekday, default=1, verbose_name="Дни недели", related_name="habits"
    )
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name="Награда")
    duration = models.DurationField(verbose_name="Время на выполнение")
    is_public = models.BooleanField(
        default=False, verbose_name="Признак публичной привычки"
    )

    # MY_CHOICES = ((1, 'Понедельник'),
    #               (2, 'Вторник'),
    #               (3, 'Среда'),
    #               (4, 'Четверг'),
    #               (5, 'Пятница'),
    #               (6, 'Суббота'),
    #               (7, 'Воскресенье'),)
    #
    # weekdays = MultiSelectField(choices=MY_CHOICES, verbose_name='Дни недели', max_length=7, max_choices=7)

    class Meta:
        verbose_name = ("Привычка",)
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"Привычка пользователя {self.owner} - я буду {self.action} в {self.time} в {self.place}"
