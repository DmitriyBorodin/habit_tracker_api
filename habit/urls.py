from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitCreateAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitDestroyAPIView,
    HabitUpdateAPIView,
    PublicHabitListAPIView,
)


app_name = HabitConfig.name

urlpatterns = [
    path("habits/", HabitListAPIView.as_view(), name="habit-list"),
    path("habits/create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("habits/<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-retrieve"),
    path("habits/<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("habits/<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit-delete"),
    path("habits/public/", PublicHabitListAPIView.as_view(), name="habit-list-public"),
]
