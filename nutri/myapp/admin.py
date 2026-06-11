from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Login)
admin.site.register(UserProfile)
admin.site.register(DonorProfile)
admin.site.register(VolunteerProfile)
admin.site.register(FoodDonation)
admin.site.register(FoodRequest)
admin.site.register(VolunteerAssignment)
admin.site.register(DistributionRecord)
admin.site.register(Feedback)
admin.site.register(Complaint)
admin.site.register(Notification)