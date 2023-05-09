from django.db import models
from students.models import Student_Profile
from lecturers.models import Lecturer_Profile
from django.contrib.auth.models import User

# Create your models here.

class Module(models.Model):
    module_code = models.CharField(max_length=10)
    module_name = models.CharField(max_length=120)
    description = models.TextField()
    lecturer = models.ForeignKey(Lecturer_Profile, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student_Profile)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.module_name

class Assessment(models.Model):
    assessment_name = models.CharField(max_length=15)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assessment_name

class Grade(models.Model):
    grade_name = models.CharField(max_length=45)
    grade_point = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.grade_name

class Score(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student_Profile, on_delete=models.CASCADE, null=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.grade