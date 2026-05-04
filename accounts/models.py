from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=50, unique=True)
    department    = models.CharField(max_length=200)
    programme     = models.CharField(max_length=200)
    level         = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.matric_number}"