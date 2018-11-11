from .models import Page
from django.contrib import admin


class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'content'),
            'description': "Feel free to use Raw HTML here.  The standard page template goes around any text you add"
        }),
    )


admin.site.register(Page, PageAdmin)
