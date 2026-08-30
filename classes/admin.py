from django.contrib import admin

from .models import SchoolClass, ClassTeacher


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):

    list_display = ['name', 'nickname', 'description']
    search_fields = ['name']


@admin.register(ClassTeacher)
class ClassTeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'school_class', 'session']
