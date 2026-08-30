from django.contrib import admin

from .models import SchoolSession, Term

@admin.register(SchoolSession)
class SchoolSessionAdmin(admin.ModelAdmin):
    list_display = ['start_year', 'end_year', 'is_current']
    list_filter = ['is_current']
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['session', 'name', 'start_date', 'end_date', 'is_current']
    list_filter = ['session', 'name', 'is_current']
    search_fields = ['name', 'session__name']


