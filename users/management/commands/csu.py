from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания суперюзера"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email="linatrofimova649@gmail.com",
            first_name="Alina",
            last_name="Alina",
            is_superuser=True,
            is_staff=True,
            is_active=True
            )

        user.set_password("1234")
        user.save()