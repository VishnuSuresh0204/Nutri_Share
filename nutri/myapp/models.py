from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------------- LOGIN ---------------- #

class Login(AbstractUser):
    userType = models.CharField(max_length=50)  # admin / donor / volunteer / user
    viewPass = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username
