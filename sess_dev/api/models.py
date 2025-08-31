from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    university = models.ForeignKey('University', on_delete=models.CASCADE,)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
