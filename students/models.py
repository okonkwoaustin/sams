from django.db import models
from classes.models import SchoolClass
from school_sessions.models import SchoolSession

class Student(models.Model):
    """Model a student"""
    GENDER_CHOICES = [
        ('Male', 'M'),
        ('Female', 'F')
    ]
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255, blank=True, null=True)
    date_of_registration = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class Parent(models.Model):
    """A parent"""
    full_name = models.CharField(max_length=60)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class StudentEnrollment(models.Model):
    """A Student enrollment"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'session']

    def __str__(self):
        return f"{self.student.first_name} - {self.date_enrolled}"

