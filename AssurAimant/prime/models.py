from django.db import models

from profilprediction.models import Prediction


class Prime(models.Model):

    prime = models.OneToOneField(Prediction, on_delete=models.CASCADE, related_name="profile2")


    def __str__(self):
        return f"{self.prime}'s Profile"
