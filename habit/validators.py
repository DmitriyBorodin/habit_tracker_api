from datetime import timedelta

from rest_framework import serializers

from habit.models import Habit


class HabitLogicValidator:
    """Проверяем логику заполнения приятной привычки, награды и связанной привычки"""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        pleasant_habit = dict(value).get('is_pleasant')
        related_habit = dict(value).get('related_habit')
        reward = dict(value).get('reward')

        if related_habit and reward:
            raise serializers.ValidationError(
                'Нельзя выбрать и приятную привычку, и награду!')

        if related_habit:
            related_habit_obj = Habit.objects.get(pk=related_habit.pk)

            if not related_habit_obj.is_pleasant:
                raise serializers.ValidationError(
                    'Связанная привычка должна быть приятной!')

        if pleasant_habit:
            if related_habit or reward:
                raise serializers.ValidationError(
                    'У приятной привычки не должно быть ни награды, ни связанной привычки!')

class DurationValidator:
    """Проверяем что время на выполнение привычки не более 120сек"""

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        time = timedelta(seconds=120)
        tmp_val = dict(value).get(self.fields)
        if tmp_val and tmp_val > time:
            raise serializers.ValidationError(
                "Время выполнения должно быть не больше 120 секунд!")