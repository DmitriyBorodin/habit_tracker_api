from rest_framework import serializers
from habit.models import Habit
from habit.validators import HabitLogicValidator, DurationValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            HabitLogicValidator(["related_habit", "reward", "is_pleasant"]),
            DurationValidator("duration"),
        ]
