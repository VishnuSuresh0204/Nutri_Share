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


# ---------------- VOLUNTEER ---------------- #

class VolunteerProfile(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    availability = models.BooleanField(default=True)
    status = models.CharField(max_length=30, default="pending")  # pending / approved / blocked
    profile_pic = models.ImageField(upload_to="volunteer_profiles", null=True, blank=True)

    def __str__(self):
        return self.name

# ---------------- FOOD DONATION ---------------- #

class FoodDonation(models.Model):
    donor = models.ForeignKey(
        DonorProfile,
        on_delete=models.CASCADE
    )

    food_name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=100)

    quantity = models.CharField(max_length=100)

    description = models.TextField()

    expiry_time = models.DateTimeField()

    pickup_address = models.TextField()

    donation_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=50,
        default="available"
    )
    # available / assigned / picked_up / delivered / cancelled

    def __str__(self):
        return self.food_name

# ---------------- FOOD REQUEST ---------------- #

class FoodRequest(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    donation = models.ForeignKey(
        FoodDonation,
        on_delete=models.CASCADE
    )

    request_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=50,
        default="pending"
    )
    # pending / approved / rejected / delivered

    def __str__(self):
        return f"{self.user.name} - {self.donation.food_name}"

# ---------------- VOLUNTEER ASSIGNMENT ---------------- #

class VolunteerAssignment(models.Model):
    donation = models.ForeignKey(
        FoodDonation,
        on_delete=models.CASCADE
    )

    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.CASCADE
    )

    assigned_date = models.DateTimeField(
        auto_now_add=True
    )

    accepted = models.BooleanField(
        null=True,
        blank=True
    )

    pickup_status = models.CharField(
        max_length=50,
        default="pending"
    )
    # pending / collected / delivered

    delivery_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.donation.food_name} - {self.volunteer.name}"

# ---------------- FOOD DISTRIBUTION RECORD ---------------- #

class DistributionRecord(models.Model):
    donation = models.ForeignKey(
        FoodDonation,
        on_delete=models.CASCADE
    )

    beneficiary = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.SET_NULL,
        null=True
    )

    distributed_at = models.DateTimeField(
        auto_now_add=True
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.donation.food_name} -> {self.beneficiary.name}"
