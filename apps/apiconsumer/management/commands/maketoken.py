from django.core.management.base import NoArgsCommand

from apiconsumer.models import APIConsumer


class Command(NoArgsCommand):
    help = "Create a token for development"

    def handle_noargs(self, **options):
        token = APIConsumer(name="public",
                            email="",
                            description="",
                            token="public",
                            permission_level=2,
                            )
        token.save()
