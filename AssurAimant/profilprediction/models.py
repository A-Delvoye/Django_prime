from django.contrib.auth.models import User
from django.db import models


class ProfilePrediction(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    REGION_CHOICES = [
        ('Northeast', 'Northeast'),
        ('Northwest', 'Northwest'),
        ('Southeast', 'Southeast'),
        ('Southwest', 'Southwest'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(default = 1)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, null=True)
    bmi = models.FloatField(default = 0)
    children = models.PositiveIntegerField(null=True)
    smoker = models.BooleanField(default = False)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, null=True)
    profile_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Profile"