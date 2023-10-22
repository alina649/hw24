from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from main.models import Course, Lesson, Payment, Subscription
from main.services import create_product, get_url
from main.validators import LinkValidator
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков"""
    # Выводим счетчик уроков
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='video_url')]


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


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели подписки пользователя на курс """

    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания платежа через Stripe """

    payment_url = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    # Можно указать это поле, если хотим указывать свою цену (не ту что в базе данных за курс или урок)
    # amount = serializers.IntegerField(required=True)

    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_url(self, obj):
        """ Получение дополнительного поля - payment_url """

        price = create_product(obj)
        return get_url(price)

    def get_price(self, payment):
        """ Получение дополнительного поля - price """

        if payment.course:
            price = payment.course.amount
        elif payment.lesson:
            price = payment.lesson.amount
        else:
            raise ValueError('Не указано за что платить, укажите ссылку на курс или урок!')
        return price




