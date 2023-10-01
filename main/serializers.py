from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from main.models import Course, Lesson
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов"""

    # Выводим счетчик уроков
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = serializers.SerializerMethodField()
    owner = SlugRelatedField(slug_field='first_name', queryset=User.objects.all())

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков"""
    class Meta:
        model = Lesson
        fields = '__all__'