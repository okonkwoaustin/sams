from django.db import models



class SchoolSession(models.Model):
    """Model a school session"""
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_current', '-start_year']

    def __str__(self):
        return f"{self.start_year}/{self.end_year}"


class Term(models.Model):
    """Model a term"""
    TERM_CHOICES = [
        ('First', "First"),
        ('Second', "Second"),
        ('Third', "Third")
    ]
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE, related_name="terms")
    name = models.CharField(max_length=10, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ("session", "name")

    def __str__(self):
        return self.name

