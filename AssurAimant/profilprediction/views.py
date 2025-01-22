from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import ProfilePredictionForm
from .models import ProfilePrediction


def home(request):
    return render(request, 'profil/test.html', {})
    #return render(request, 'base_.html', {})
"""
# Page d'accueil
def home(request):
    return render(request, 'AssurAimant/base_html')
"""
# Gestion du profil utilisateur
@login_required
def profileprediction(request):
    # Récupérer ou créer un profil pour l'utilisateur connecté
    #user_profile, created = ProfilePrediction.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePredictionForm(request.POST)
        if form.is_valid():
            #form.save(commit=False)
            print(form.cleaned_data)
            user_profile, created = ProfilePrediction.objects.get_or_create(
                user = request.user,
               # profile_updated_at = form.cleaned_data["age"],
            )
            #if created:
            user_profile.age=form.cleaned_data["age"]
            user_profile.sex = form.cleaned_data["sex"]
            user_profile.bmi = form.cleaned_data["bmi"]
            user_profile.children = form.cleaned_data["children"]
            user_profile.smoker = form.cleaned_data["smoker"]
            user_profile.region = form.cleaned_data["region"]
            user_profile.save()

            #form.save(commit=True)
            print(user_profile)
            return redirect('home')  # Redirige après enregistrement
    else:
        form = ProfilePredictionForm()

    return render(request, 'profilprediction/test.html', {'form': form})

class CustomConnexion(LoginView):
    template_name = "profilprediction/login.html"

