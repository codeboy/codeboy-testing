from django.core.management.base import BaseCommand

from django.db.models.signals import post_syncdb
from django.contrib.auth.management import create_superuser

from django.contrib.auth.models import User


class Command(BaseCommand):

    username = 'admin'
    email = 'developer.ru@gmail.com'
    password = 321

    def handle(self, *args, **options):

        try:
            b = User.objects.get(pk = 1)
        except :
            try :
                User.objects.create_superuser(self.username, self.email, self.password)
#                create_superuser(username, email, password)
                self.stdout.write("Superuser created successfully.\n")
            except :
                self.stdout.write("Superuser NOT created.\n")
