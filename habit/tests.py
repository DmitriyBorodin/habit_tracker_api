from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit, Weekday
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        # Пользователи
        self.user1 = User.objects.create(email="user1@test.pro")
        self.user2 = User.objects.create(email="user2@test.pro")

        # День недели
        self.weekday = Weekday.objects.create(day="Понедельник", number=1)

        # Привычка
        self.habit_u1 = Habit.objects.create(
            action="habit_1",
            place="place_1",
            time="00:10:00",
            owner=self.user1,
            duration="00:02:00",
        )
        self.habit_u1.weekdays.add(self.weekday)

        # Приятные привычка
        self.habit_u2 = Habit.objects.create(
            action="habit_2",
            place="place_2",
            time="00:21:00",
            owner=self.user2,
            duration="00:01:00",
            is_pleasant=True,
        )
        self.habit_u2.weekdays.add(self.weekday)

        # Публичная привычка
        self.habit_is_public = Habit.objects.create(
            action="habit_3",
            place="place_3",
            time="00:11:00",
            owner=self.user2,
            is_public=True,
            duration="00:02:00",
        )
        self.habit_is_public.weekdays.add(self.weekday)

    def test_habit_retrieve(self):
        """Проверяем просмотр привычки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-retrieve", args=(self.habit_u1.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(data.get("action"), self.habit_u1.action)

    def test_habit_update(self):
        """Проверяем обновление привычки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-update", args=(self.habit_u1.pk,))
        data = {"action": "update_habit"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "update_habit")

    def test_habit_delete(self):
        """Проверяем удаление привычки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-delete", args=(self.habit_u1.pk,))
        response = self.client.delete(url)
        # Проверяем, что ответ имеет статус 204
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Habit.DoesNotExist):
            Habit.objects.get(pk=self.habit_u1.pk)

    def test_habit_list(self):
        """Проверяем просмотр списка привычек"""

        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-list")
        response = self.client.get(url)
        data = response.json()
        weekdays_ids = [self.weekday.pk]
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit_u1.pk,
                    "action": self.habit_u1.action,
                    "place": self.habit_u1.place,
                    "time": self.habit_u1.time,
                    "is_pleasant": self.habit_u1.is_pleasant,
                    "related_habit": self.habit_u1.related_habit,
                    "weekdays": weekdays_ids,
                    "owner": self.habit_u1.owner.pk,
                    "reward": self.habit_u1.reward,
                    "duration": self.habit_u1.duration,
                    "is_public": self.habit_u1.is_public,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_is_public_list(self):
        """Проверяем просмотр списка опубликованных привычек"""

        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-list-public")
        response = self.client.get(url)
        data = response.json()
        weekdays_ids = [self.weekday.pk]
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit_is_public.pk,
                    "action": self.habit_is_public.action,
                    "place": self.habit_is_public.place,
                    "time": self.habit_is_public.time,
                    "is_pleasant": self.habit_is_public.is_pleasant,
                    "related_habit": self.habit_is_public.related_habit,
                    "weekdays": weekdays_ids,
                    "owner": self.habit_is_public.owner.pk,
                    "reward": self.habit_is_public.reward,
                    "duration": self.habit_is_public.duration,
                    "is_public": self.habit_is_public.is_public,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_list_for_unauthorized_user(self):
        """Проверяем просмотр списка привычек неавторизованным пользователем"""
        url = reverse("habit:habit-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data, {"detail": "Учетные данные не были предоставлены."})

    def test_habit_is_public_list_for_unauthorized_user(self):
        """Проверяем просмотр списка опубликованных привычек неавторизованным пользователем"""
        url = reverse("habit:habit-list-public")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(data, {"detail": "Учетные данные не были предоставлены."})

    def test_habit_create(self):
        """Проверяем создание привычки"""

        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-create")
        weekdays_ids = [self.weekday.pk]
        data = {
            "action": "new_habit",
            "place": "new_place",
            "time": "16:00:00",
            "duration": "00:02:00",
            "weekdays": weekdays_ids,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 4)

    def test_pleasant_habit_create(self):
        """Проверяем создание приятной привычки"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-create")
        weekdays_ids = [self.weekday.pk]
        data = {
            "action": "new_habit",
            "place": "new_place",
            "time": "16:00:00",
            "duration": "00:02:00",
            "weekdays": weekdays_ids,
            "is_pleasant": True,
            "reward": "test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "У приятной привычки не должно быть ни награды, ни связанной привычки!"
                ]
            },
        )

    def test_habit_create_with_reward(self):
        """Проверяем создание привычки c вознаграждением"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-create")
        weekdays_ids = [self.weekday.pk]
        data = {
            "action": "new_habit",
            "place": "new_place",
            "time": "16:00:00",
            "duration": "00:02:00",
            "weekdays": weekdays_ids,
            "is_pleasant": False,
            "related_habit": self.habit_u2.pk,
            "reward": "test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Нельзя выбрать и приятную привычку, и награду!"]},
        )

    def test_habit_create_with_invalid_related_habit(self):
        """Проверяем создание привычки c невалидной связанной привычкой"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-create")
        weekdays_ids = [self.weekday.pk]
        data = {
            "action": "new_habit",
            "place": "new_place",
            "time": "16:00:00",
            "duration": "00:02:00",
            "weekdays": weekdays_ids,
            "related_habit": self.habit_u1.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"non_field_errors": ["Связанная привычка должна быть приятной!"]},
        )

    def test_habit_create_with_invalid_time(self):
        """Проверяем создание привычки c невалидным временем выполнения"""
        self.client.force_authenticate(user=self.user1)
        url = reverse("habit:habit-create")
        weekdays_ids = [self.weekday.pk]
        data = {
            "action": "new_habit",
            "place": "new_place",
            "time": "16:00:00",
            "duration": "00:30:00",
            "weekdays": weekdays_ids,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Время выполнения должно быть не больше 120 секунд!"
                ]
            },
        )
