from django.db import models
from django.contrib.auth.models import User

class Rendezvous(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    jour = models.PositiveIntegerField(default = 1)
    mois = models.PositiveIntegerField(default = 1)
    annee = models.PositiveIntegerField(default = 2025)

    def __str__(self):
        return f"{self.user}'s Profile"