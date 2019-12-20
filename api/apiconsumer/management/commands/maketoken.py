from django.core.management.base import BaseCommand

from api.apiconsumer.models import APIConsumer


class Command(BaseCommand):
    help = 'Create a token for development'

    def handle(self, **options):
        APIConsumer.objects.get_or_create(token='public', defaults={
            'name': 'Public',
            'email': '',
            'description': '',
            'permission_level': 2
        })
