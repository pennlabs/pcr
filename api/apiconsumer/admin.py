from .models import APIConsumer, APIUser
from django.contrib import admin

# TODO - don't use all models
admin.site.register(APIConsumer)
admin.site.register(APIUser)
