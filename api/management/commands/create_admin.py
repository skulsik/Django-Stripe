from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    """ Создание суперпользователя """
    def handle(self, *args, **options):
        if not User.objects.count():
            username = 'admin'
            email = 'admin@pochta.ru'
            password = 'admin'
            print('Создание учетной записи суперпользователя для %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Учетная запись суперпользователя существует!')
