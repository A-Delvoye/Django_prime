import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import ProfilePredictionForm
from .models import ProfilePrediction, Prediction

from .utils import load_model

# Chargez le modèle au démarrage
MODEL_PATH = "profilprediction/templates/profilprediction/ElasticNet_model_fit_2.pkl"
insurance_model = load_model(MODEL_PATH)


# Gestion du profil utilisateur
@login_required
def profileprediction(request):

    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect('home')

        form = ProfilePredictionForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("2311")
            #form.save(commit=False)
            print(form.cleaned_data)
            user_profile, created = ProfilePrediction.objects.get_or_create(
                user = request.user,
            )
            user_profile.age=form.cleaned_data["age"]
            user_profile.sex = form.cleaned_data["sex"]
            user_profile.bmi = form.cleaned_data["bmi"]
            user_profile.children = form.cleaned_data["children"]
            user_profile.smoker = form.cleaned_data["smoker"]
            user_profile.region = form.cleaned_data["region"]
            user_profile.save()

            print(user_profile)

            return redirect('home')  # Redirige après enregistrement
    else:
        try:
            profile = ProfilePrediction.objects.get(user=request.user)
            form = ProfilePredictionForm(initial={
                'age': profile.age,
                'sex': profile.sex,
                'bmi': profile.bmi,
                'children': profile.children,
                'smoker': profile.smoker,
                'region': profile.region,
            })
        except ProfilePrediction.DoesNotExist:
            form = ProfilePredictionForm()

    return render(request, 'profilprediction/profile.html', {'form': form})

class CustomConnexion(LoginView):
    #template_name = "profilprediction/login.html"
    pass

def calculate_prime(age, bmi, sex, children, smoker, region):
    """
    Simulation du calcul de la prime d'assurance.
    """
    sex_mapping = {"Male": "male", "Female": "female"}
    smoker_mapping = {0: "yes", 1: "no"}
    region_mapping = {"Southeast": "southeast", "Northwest": "northwest", "Northeast": "northeast",
                      "Southwest": "southwest"}

    # Mapper les valeurs d'entrée
    sex = sex_mapping[sex]
    smoker = smoker_mapping[smoker]
    region = region_mapping[region]

    bmi_smoker = bmi * (1 if smoker == "yes" else 0)
    age_smoker = age * (1 if smoker == "yes" else 0)
    age_bmi = age * bmi

    # Groupes d'âge et catégories BMI
    bins_age = [0, 28, 51, 65, np.inf]
    labels_age = ['Jeune', 'Mature', 'Âgé', 'Senior']

    bins_bmi = [0, 18, 30, 40, np.inf]
    labels_bmi = ['Maigre', 'Normal', 'Surpoids', 'Obèse']

    # Trouver les groupes d'âge et de BMI
    age_group = labels_age[np.digitize(age, bins_age, right=False) - 1]
    bmi_category = labels_bmi[np.digitize(bmi, bins_bmi, right=False) - 1]

    # Préparer les données d'entrée sous forme de DataFrame pandas
    input_data = {
        "age": [age],
        "sex": [sex],
        "bmi": [bmi],
        "children": [children],
        "smoker": [smoker],
        "region": [region],
        "age_group": [age_group],
        "bmi_category": [bmi_category],
        "bmi_smoker": [bmi_smoker],
        "age_smoker": [age_smoker],
        "age_bmi": [age_bmi]
    }

    # Convertir en DataFrame
    input_df = pd.DataFrame(input_data)

    try:
        # Effectuer la prédiction
        prediction = insurance_model.predict(input_df)
        return prediction[0]  # Retourner la première prédiction
    except Exception as e:
        print(f"Erreur lors de la prédiction : {e}")
        return None


@login_required
def prediction_page(request):
    # Charge le profil utilisateur existant
    try:
        profile = ProfilePrediction.objects.get(user=request.user)
    except ProfilePrediction.DoesNotExist:
        return redirect('profileprediction')  # Redirige vers le formulaire de profil si pas de profil

    if request.method == 'POST':
        # Simule et enregistre une prédiction
        prime = calculate_prime(
            age=profile.age,
            bmi=profile.bmi,
            sex = profile.sex,
            children=profile.children,
            smoker=profile.smoker,
            region=profile.region,
        )
        # Enregistre la prédiction
        Prediction.objects.create(profile=profile, prime=prime)

        return render(request, 'profilprediction/prime_resultat.html', {'prime': prime})

    return render(request, 'profilprediction/prime_simulation.html', {'profile': profile})

@login_required
def prediction_history(request):
    try:
        profile = ProfilePrediction.objects.get(user=request.user)
    except ProfilePrediction.DoesNotExist:
        return redirect('profileprediction')  # Redirige si aucun profil n'existe

    predictions = profile.predictions.all()  # Récupère toutes les prédictions associées au profil
    return render(request, 'profilprediction/historique.html', {'profile': profile, 'predictions': predictions})

