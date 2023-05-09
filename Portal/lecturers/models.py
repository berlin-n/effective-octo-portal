from django.db import models
from django.contrib.auth.models import User



# Create your models here.

choices = (
    ('Student', 'Student'),
    ('Lecturer', 'Lecturer')
)

class Lecturer_Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20 ,choices=choices, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name + " " +self.first_name
    

