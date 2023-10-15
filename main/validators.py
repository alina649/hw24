import re
from rest_framework.serializers import ValidationError


class LinkValidator:
    """Валидация ссылки на материалы (только youtube) """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value and not 'youtube.com' in tmp_value:
            raise ValidationError('Ссылка может быть только на ютуб')