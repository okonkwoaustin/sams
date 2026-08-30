from django.contrib import admin
from .models import Attendance, AttendanceRecord
from students.models import StudentEnrollment


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['school_class', 'term', 'date', 'teacher']
    list_filter = ['term', 'school_class', 'date']
    search_fields = ['school_class__name', 'teacher__username']
    date_hierarchy = 'date'
    ordering = ['-date']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.teacher = request.user
        super().save_model(request, obj, form, change)


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_enrollment', 'attendance', 'status', 'time_stamp']
    list_filter = ['status', 'attendance__term', 'attendance__school_class']
    search_fields = ['student__first_name', 'student__last_name', 
                     'student__admission_number']
    ordering = ['-attendance__date']


