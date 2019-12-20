from django.core.management.base import BaseCommand

from api.apiconsumer.models import APIConsumer


class Command(BaseCommand):
    help = 'Create a token for development'

    def handle(self, **options):
        token = APIConsumer(name='public',
                            email='',
                            description='',
                            token='public',
                            permission_level=2,
                            )
        token.save()
