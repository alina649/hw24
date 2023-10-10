from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from main.models import Course, Lesson, Payment
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков"""
    # Выводим счетчик уроков
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели урока для использования его в выводе в курсах """

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)

    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    # Выводим имя пользователя в поле "owner", вместо цифры
    owner = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

        # Получаем все поля для дополнительного поля уроков с фильтрацией по курсу
        def get_lessons(self, course):
            return LessonListSerializer(Lesson.objects.filter(course=course), many=True, read_only=True).data


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели платежей """

    class Meta:
        model = Payment
        fields = '__all__'