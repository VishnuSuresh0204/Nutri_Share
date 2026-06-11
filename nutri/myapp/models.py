from django.db import models
from django.contrib.auth.models import AbstractUser

# ---------------- LOGIN ---------------- #

class Login(AbstractUser):
    userType = models.CharField(max_length=50)  # admin / donor / volunteer / user
    viewPass = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username


# ---------------- BENEFICIARY(USER) ---------------- #

class UserProfile(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to="user_profiles", null=True, blank=True)

    def __str__(self):
        return self.name


# ---------------- DONOR ---------------- #

class DonorProfile(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=200)
    donor_type = models.CharField(max_length=50)  # Restaurant / Hotel / Supermarket / Household
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=30, default="pending")  # pending / approved / rejected
    logo = models.ImageField(upload_to="donor_logos", null=True, blank=True)

    def __str__(self):
        return self.organization_name
