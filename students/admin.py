from django.contrib import admin
from .models import Student, Parent, StudentEnrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'first_name', 'middle_name', 'last_name', 
                    'date_of_birth', 'gender', 'address', 'date_of_registration']
    list_filter = ['first_name', 'last_name']
    search_fields = ['admission_number', 'first_name', 'last_name']
    ordering = ['-date_of_registration', 'last_name', 'first_name']
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student']

@admin.register(StudentEnrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'school_class', 'session', 'date_enrolled']
    list_filter = ['session', 'school_class']
    search_fields = ['student__first_name', 'student__last_name', 
                     'student__admission_number']
    ordering = ['-session', 'school_class']

