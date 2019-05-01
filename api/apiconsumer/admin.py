from .models import APIConsumer, APIUser
from django.contrib import admin


class APIConsumerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_filter = ('permission_level',)


class APIUserAdmin(admin.ModelAdmin):
    search_fields = ('username',)


admin.site.register(APIConsumer, APIConsumerAdmin)
admin.site.register(APIUser, APIUserAdmin)
