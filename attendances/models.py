from django.db import models
from classes.models import SchoolClass
from school_sessions.models import Term
from django.conf import settings
from students.models import StudentEnrollment


class Attendance(models.Model):
    """Attendance object"""
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    date = models.DateTimeField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        blank=True, editable=False)

    class Meta:
        unique_together = ['school_class', 'date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'

    def __str__(self):
        return f"{self.school_class} - {self.date.strftime('%d-%m-%Y %H:%M:%S')}"

class AttendanceRecord(models.Model):
    """An attendance record"""
    STATUS_CHOICES = [
        ('Present', 'P'),
        ('Absent', 'A'),
        ('Late', 'L'),
        ('Excused', 'E'),
    ] 
    
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, 
                                   related_name='records')
    student_enrollment = models.ForeignKey(StudentEnrollment, 
                                           on_delete=models.CASCADE)
        
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)
    remarks = models.CharField(max_length=150, blank=True, null=True)
    time_stamp = models.TimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['attendance', 'student_enrollment']

    
        

