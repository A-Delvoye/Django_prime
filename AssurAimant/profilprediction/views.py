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
            form.save(commit=False)
            print(form.cleaned_data)
            user_profile, created = ProfilePrediction.objects.get_or_create(
                user=request.user,
                age=form.cleaned_data["age"],
                sex = form.cleaned_data["sex"],
                bmi = form.cleaned_data["bmi"],
                children = form.cleaned_data["children"],
                smoker = form.cleaned_data["smoker"],
                region = form.cleaned_data["region"],
               # profile_updated_at = form.cleaned_data["age"],
            )
            print(user_profile)
           # return redirect('profile2')  # Redirige après enregistrement
    else:
        form = ProfilePredictionForm()

    return render(request, 'profilprediction/test.html', {'form': form})

class CustomConnexion(LoginView):
    template_name = "profilprediction/login.html"

