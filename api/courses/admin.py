from django.contrib import admin
from django.http import HttpResponse
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from .models import Instructor, Course, Section, Review


admin.site.unregister(Group)
admin.site.unregister(Site)


class InstructorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('primary_alias', 'semester', 'name')
    list_select_related = True
    search_fields = ('primary_alias__department__code',
                     'primary_alias__coursenum', 'name', 'description',)
    ordering = ('-semester', 'primary_alias')
    raw_id_fields = ('primary_alias', 'history',)

    def get_urls(self):
        urls = super(CourseAdmin, self).get_urls()
        my_urls = [
            url(r'^generate_cache/$', lambda request: HttpResponse("you clicked generate cache")),
            url(r'^push_to_live/$', lambda request: HttpResponse("you clicked push to live"))
        ]
        return my_urls + urls


class SectionAdmin(admin.ModelAdmin):
    list_display = ('course_alias', 'name', 'sectionnum', 'semester')
    list_select_related = True
    search_fields = ('name', 'sectionnum', 'course__name',)
    ordering = ('-course__semester', 'name', 'sectionnum')
    raw_id_fields = ('course', 'instructors',)

    def course_alias(self, obj):
        return obj.course.primary_alias

    def semester(self, obj):
        return obj.course.semester


class ReviewAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('primary_alias', 'sectionnum',
                    'instructor', 'section', 'semester')
    list_display_links = ('primary_alias', 'sectionnum', 'instructor',)
    search_fields = ('section__course__primary_alias__department__code', 'section__course__primary_alias__coursenum',
                     'section__course__name', 'section__name', '^instructor__first_name', '^instructor__last_name')
    ordering = ('-section__course__semester', 'section')
    raw_id_fields = ('section', 'instructor')

    def primary_alias(self, obj):
        return obj.section.course.primary_alias

    def semester(self, obj):
        return obj.section.course.semester
    semester.admin_order_field = 'section__course__semester'

    def course(self, obj):
        return obj.section.course.name

    def sectionnum(self, obj):
        return obj.section.sectionnum


admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Review, ReviewAdmin)

"""
 add urls to some Admin's get_urls(self)
 a la the end of http://djangosnippets.org/snippets/1936/

 Make it fire towards some custom python script that Matt has.

 As a result, hitting either of the 'generate cache' / 'push live' buttons
 will be forwarded to matt's scripts here.

"""
