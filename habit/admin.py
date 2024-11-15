from django.contrib import admin

from habit.models import Habit, Weekday


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "owner", "is_public")


@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    list_display = ("id", "day", "number")
