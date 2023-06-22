from django.core.management.base import BaseCommand

from core.models import CustomUser


class Command(BaseCommand):
    help = 'Resets the number of instant searches for all users to 3'

    def handle(self, *args, **options):
        CustomUser.objects.all().update(instant_searches_left=3)
        self.stdout.write(self.style.SUCCESS('Successfully reset instant searches for all users.'))
