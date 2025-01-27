from django.shortcuts import render

# Create your views here.
from .models import Prime
from profilprediction.models import Prediction

def ma_vue(request):
    pred = Prediction.objects.first()
    prime = Prime.objects.get_or_create(prime=pred)
    render("prime/test.html", request, context={})