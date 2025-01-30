import numpy as np
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import ProfilePredictionForm
from .models import ProfilePrediction, Prediction
from django.contrib import messages
from django.core.mail import EmailMessage
from fpdf import FPDF
from django.http import FileResponse
import os
from .utils import load_model

# Chargez le modèle au démarrage
MODEL_PATH = "profilprediction/templates/profilprediction/ElasticNet_model_fit_2.pkl"
insurance_model = load_model(MODEL_PATH)

# Gestion du profil utilisateur
@login_required
def profileprediction(request):

    """
    profileprediction: Cette fonction permet de charger le formulaire de prédiction et se rediriger

    """
    if request.method == 'POST':

        if 'cancel' in request.POST:
            return redirect('home')

        form = ProfilePredictionForm(request.POST)
        print(request.POST)
        if form.is_valid():
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
    """
    profileprediction: Cette fonction permet de calculer la prime et de diriger

    vers la page de résultats de prédiction.

    """
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
        return redirect('profileprediction')  # Redirige vers le formulaire de profil si pas de profil

    if request.method == 'POST':
        # Simule et enregistre une prédiction
        form = ProfilePredictionForm(request.POST)

        if form.is_valid():
            raw_data = {
                'age': form.cleaned_data["age"],
                'bmi': form.cleaned_data["bmi"],
                'children': form.cleaned_data["children"],
                'sex': form.cleaned_data["sex"],
                'smoker': form.cleaned_data["smoker"],
                'region': form.cleaned_data["region"]
            }
            age, bmi, sex, children, smoker, region = transform_input_data(raw_data)

            prime = calculate_prime(
                age = age,
                bmi = bmi,
                sex = sex,
                children = children,
                smoker = smoker,
                region = region,
            )
            # Enregistre la prédiction
            Prediction.objects.create(profile=profile,
                                      prime=prime,
                                      age = age,
                                      bmi = bmi,
                                      sex = sex,
                                      children = children,
                                      smoker = smoker,
                                      region = region)

            if "generer" in request.POST:
                pdf_path = generate_pdf(age, bmi, sex, children, smoker, region, prime)
                return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')

            elif "envoyer e-mail" in request.POST:
                print(request.POST)
                user = request.user
                email = user.email  # "destinataire@gmail.com"
                print(email)
                send_email_with_pdf(email, age, bmi, sex, children, smoker, region, prime)
                messages.success(request, "Votre email a été envoyé avec succès.")
                #generate_mail_link(request)

            else:
                # Calculer la prime et afficher les résultats
                return render(request, 'profilprediction/prime_simulation.html', {
                    'form': form,
                    'prime': prime,
                })
    return render(request, 'profilprediction/prime_simulation.html', {'form': form})

@login_required
def prediction_history(request):
    """prediction_history: the prediction history of the user

        Returns: rediriger vers la page historique
    """
    search_query = request.GET.get('q', '').strip()  # Récupère et nettoie la recherch

    try:
        profile = ProfilePrediction.objects.get(user=request.user)
    except ProfilePrediction.DoesNotExist:
        return redirect('profileprediction')  # Redirige si aucun profil n'existe

    if request.user.is_staff:
        predictions = Prediction.objects.all()  # Récupère toutes les prédictions de tous les profils
    else:
        predictions = profile.predictions.all()
    
    if search_query:
            predictions = predictions.filter(profile__user__username__icontains=search_query)
    
    return render(request, 'profilprediction/historique.html', {'profile': profile, 'predictions': predictions})



def transform_input_data(data):
    """
    Transforme les données d'entrée pour qu'elles soient compatibles avec la fonction calculate_prime.
    """
    # Extraction des valeurs et conversion dans le bon type
    age = int(data['age'])  # Convertir en entier
    bmi = float(data['bmi'])  # Convertir en float
    children = int(data['children'])  # Convertir en entier
    sex = data['sex'].capitalize()  # Normaliser (majuscule initiale)
    smoker = data['smoker'].capitalize() == 'True'  # Normaliser et convertir en booléen
    region = data['region'].capitalize()  # Normaliser (majuscule initiale)

    # Mapping des valeurs
    smoker_mapping = {True: 0, False: 1}
    smoker = smoker_mapping[smoker]

    # Retourner les valeurs transformées
    return age, bmi, sex, children, smoker, region

def generate_pdf(age, bmi, sex, children, smoker, region, prime):
    """
    Génère un fichier PDF avec les détails de la simulation.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Ajouter un titre
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Simulation de Prime d'Assurance", ln=True, align='C')
    pdf.ln(10)

    # Ajouter les détails
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Âge: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Indice de Masse Corporelle (BMI): {bmi}", ln=True)
    pdf.cell(200, 10, txt=f"Sexe: {sex}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'enfants: {children}", ln=True)
    pdf.cell(200, 10, txt=f"Fumeur: {'Oui' if smoker == 'yes' else 'Non'}", ln=True)
    pdf.cell(200, 10, txt=f"Région: {region}", ln=True)
    pdf.cell(200, 10, txt=f"Prime estimée: {prime:.2f} euros", ln=True)

    # Sauvegarder le PDF
    pdf_file_path = "simulation_prime.pdf"
    pdf.output(pdf_file_path)
    return pdf_file_path


def view_pdf(request, age, bmi, sex, children, smoker, region):
    """
    Génère et retourne un PDF pour la prévisualisation.
    """
    # Calculer la prime
    prime = calculate_prime(age, bmi, sex, children, smoker, region)

    # Générer le PDF
    pdf_path = generate_pdf(age, bmi, sex, children, smoker, region, prime)

    # Retourner le PDF pour téléchargement
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')


def send_email_with_pdf(to_email, age, bmi, sex, children, smoker, region, prime):
    """
    Envoie un e-mail avec le fichier PDF de simulation en pièce jointe.
    """
        # Générer le PDF
    pdf_path = generate_pdf(age, bmi, sex, children, smoker, region, prime)
    print("eeedr",to_email)
    # Créer l'e-mail
    email = EmailMessage(
        subject="Simulation de Prime d'Assurance",
        body="Veuillez trouver ci-joint le fichier PDF de votre simulation de prime d'assurance.",
        to=[to_email],
    )
    print(email)
    # Attacher le fichier PDF
    email.attach_file(pdf_path)

    # Envoyer l'e-mail
    email.send()
    

@login_required
def developer_dashboard(request):
    
    """
    Page dédiée aux développeurs, listant toutes les fonctionnalités de l'application.
    Accessible uniquement aux administrateurs et développeurs.
    """
    #if not request.user.is_staff:  # Vérifie si l'utilisateur est un développeur/admin
    #    return redirect('home')  # Redirige l'utilisateur vers la page d'accueil s'il n'est pas développeur

    # Liste des fonctionnalités
    features = [
        {
            "name": "profileprediction",
            "description": "Permet de charger le formulaire de prédiction et de rediriger l'utilisateur après soumission.",
        },
        {
            "name": "calculate_prime",
            "description": "Calcule la prime d'assurance en fonction des données fournies.",
        },
        {
            "name": "prediction_page",
            "description": "Affiche la page de simulation des primes avec les résultats.",
        },
        {
            "name": "prediction_history",
            "description": "Affiche l'historique des prédictions d'un utilisateur.",
        },
        {
            "name": "transform_input_data",
            "description": "Transforme les données brutes d'entrée pour les rendre compatibles avec la prédiction.",
        },
        {
            "name": "generate_pdf",
            "description": "Génère un fichier PDF contenant les détails d'une simulation.",
        },
        {
            "name": "view_pdf",
            "description": "Affiche un fichier PDF généré pour prévisualisation ou téléchargement.",
        },
        {
            "name": "send_email_with_pdf",
            "description": "Envoie un e-mail avec la simulation en pièce jointe au format PDF.",
        },
    ]

    return render(request, 'profilprediction/developer_dashboard_.html', {'features': features})