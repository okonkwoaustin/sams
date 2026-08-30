from django.db import models
from school_sessions.models import SchoolSession
from django.conf import settings


class SchoolClass(models.Model):
    """Model a Class object"""
    CLASS_CHOICES = [
        ('Grade One', 'Grade 1'),
        ('Grade Two', 'Grade 2'),
        ('Grade Three', 'Grade 3'),
        ('Grade Four', 'Grade 4'),
        ('Grade Five', 'Grade 5'),
        ('Grade Six', 'Grade 6'),
    ]
    name = models.CharField(max_length=20, choices=CLASS_CHOICES)
    nickname = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'School Class'
        verbose_name_plural = 'School Classes'
        pass
    
    def __str__(self):
        return self.name
    

class ClassTeacher(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school_class = models.OneToOneField(SchoolClass, on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)
