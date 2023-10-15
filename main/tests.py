from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from main.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """ Тестирование уроков - Lesson """

    def setUp(self):
        """ Тестовые настройки для создания экземпляров моделей """

        self.user = User.objects.create(email='admin', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(course_name='TestCourse', course_description='TestCourseDescription')
        self.lesson = Lesson.objects.create(
            course=self.course,
            lesson_name='TestLesson',
            lesson_description='TestLessonDescription',
            video_url='https://youtube.com',
            owner=self.user,
        )

    def test_lesson_create(self):
        """ Тестирование создания урока """

        expected_data = {
            "course": self.course.pk,
            "lesson_name": "TEST1",
            "lesson_description": "TEST1",
            "video_url": "https://youtube.com",
            "owner": self.user.pk
        }
        response = self.client.post(
            reverse('main:lesson_create'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "course": self.course.pk,
                "lesson_name": "TEST1",
                "lesson_description": "TEST1",
                "lesson_preview": None,
                "video_url": self.lesson.video_url,
                "owner": self.user.pk
            }
        )

    def test_lesson_list(self):
        """ Тестирование вывода списка уроков """

        response = self.client.get(
            reverse('main:lesson_list'),
            HTTP_AUTHORIZATION=self.token
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "course": self.course.pk,
                        "lesson_name": self.lesson.lesson_name,
                        "lesson_description": self.lesson.lesson_description,
                        "lesson_preview": None,
                        "video_url": self.lesson.video_url,
                        "owner": self.user.pk
                    }
                ]
            }
        )

    def test_lesson_retrieve(self):
        """ Тестирование вывода одного урока """

        response = self.client.get(
            reverse('main:lesson_detail', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.pk,
                "lesson_name": self.lesson.lesson_name,
                "lesson_description": self.lesson.lesson_description,
                "lesson_preview": None,
                "video_url": self.lesson.video_url,
                "owner": self.user.pk
            }
        )

    def test_lesson_update(self):
        """ Тестирование обновления урока """

        # Первый вариант обновления данных
        expected_data = {
            "course": self.course.pk,
            "lesson_name": "TEST2",
            "video_url": "https://youtube.com/test2/"
        }
        response = self.client.patch(
            reverse('main:lesson_update', kwargs={'pk': self.lesson.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.pk,
                "lesson_name": "TEST2",
                "lesson_description": self.lesson.lesson_description,
                "lesson_preview": None,
                "video_url": "https://youtube.com/test2/",
                "owner": self.user.pk
            }
        )

        # Второй вариант обновления данных
        expected_data = {
            "course": self.course.pk,
            "lesson_name": "TEST3",
            "lesson_description": "TEST3",
            "video_url": "https://youtube.com/test3/"
        }

        response = self.client.put(
            reverse('main:lesson_update', kwargs={'pk': self.lesson.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "course": self.course.pk,
                "lesson_name": "TEST3",
                "lesson_description": "TEST3",
                "lesson_preview": None,
                "video_url": "https://youtube.com/test3/",
                "owner": self.user.pk
            }
        )

    def test_lesson_destroy(self):
        """ Тестирование удаления урока """

        response = self.client.delete(
            reverse('main:lesson_delete', kwargs={'pk': self.lesson.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Lesson.objects.all()),
            []
        )

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.lesson.delete()


class SubscriptionTestCase(APITestCase):
    """ Тестирование подписки на курс """

    def setUp(self):
        """ Тестовые настройки создание экземпляров моделей """

        self.user = User.objects.create(email='admin', password='admin', is_superuser=True)
        self.token = f'Bearer {AccessToken.for_user(self.user)}'
        self.course = Course.objects.create(course_name="TEST", course_description="TEST", owner=self.user)

        self.data = {
            'user': self.user,
            'course': self.course,
        }

        self.subscription = Subscription.objects.create(**self.data)

    def test_create_subscription(self):
        """ Тестирование подписки на курс """

        expected_data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'is_subscribed': True
        }

        response = self.client.post(
            reverse('main:subscription-list'),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            2
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "is_subscribed": True,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_unsubscribe(self):
        """ Тестирование отписки на курс """

        expected_data = {
            'user': self.user.pk,
            'course': self.course.pk,
            'is_subscribed': False
        }

        response = self.client.patch(
            reverse('main:subscription-detail', kwargs={'id': self.subscription.pk}),
            data=expected_data,
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            1
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.subscription.pk,
                "is_subscribed": False,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_list_subscription(self):
        """ Тестирование списка подписок """

        response = self.client.get(
            reverse('main:subscription-list'),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            1
        )

    def test_subscription_retrieve(self):
        """ Тестирование вывода одной подписки """

        response = self.client.get(
            reverse('main:subscription-detail', kwargs={'id': self.subscription.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.subscription.pk,
                "is_subscribed": False,
                "user": self.user.pk,
                "course": self.course.pk
            }
        )

    def test_subscription_destroy(self):
        """ Тестирование удаления подписки """

        response = self.client.delete(
            reverse('main:subscription-detail', kwargs={'id': self.subscription.pk}),
            HTTP_AUTHORIZATION=self.token
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            list(Subscription.objects.all()),
            []
        )

    def tearDown(self):
        self.user.delete()
        self.course.delete()
        self.subscription.delete()

