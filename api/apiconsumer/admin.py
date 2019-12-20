from django.contrib import admin

from .models import APIConsumer


class APIConsumerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_filter = ('permission_level',)


admin.site.register(APIConsumer, APIConsumerAdmin)
