from rest_framework import serializers
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from main.models import Course, Lesson
from main.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели обучающего курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    class Meta:
        model = Course
        fields = '__all__'


class LessonCreateAPIView(generics.CreateAPIView):
    """Generic-класс для создания объекта модели Lesson"""
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Generic-класс для просмотра всех объектов Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Generic-класс для просмотра одного объекта Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Generic-класс для обновления объекта Lesson"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Generic-класс для удаления одного объекта Lesson"""
    queryset = Lesson.objects.all()

