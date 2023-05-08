from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth.hashers import make_password

from manager_app.models import CustomUser
from django.conf import settings

from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = "This command creates default admin user"

    def handle(self, *args, **options):
        try:
            CustomUser.objects.create_superuser(email=settings.ADMIN_LOGIN, password=settings.ADMIN_PASSWORD)
        except IntegrityError:
            print('Admin is already exists')
            return
        self.stdout.write('Admin was created')
