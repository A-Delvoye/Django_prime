from django.core.exceptions import ValidationError
from django import forms

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

class ProfilePredictionForm(forms.Form):


    age = forms.IntegerField(
        label="Âge",
        min_value=18,
        max_value=120,
        help_text="Entrez un âge entre 18 et 120 ans.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Âge', 'id': 'age'}),
    )
    bmi = forms.FloatField(
        label="BMI",
        min_value=10,
        max_value=60,
        help_text="Entrez un BMI entre 10 et 60.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'BMI', 'id': 'bmi'}),
    )
    children = forms.IntegerField(
        label="Nombre d'enfants",
        min_value=0,
        max_value=10,
        help_text="Entrez un nombre d'enfants entre 0 et 20.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre d\'enfants', 'id': 'children'}),
    )
    sex = forms.ChoiceField(
        label="Sexe",
        choices=SEX_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )
    smoker = forms.ChoiceField(
        label="Fumeur",
        choices=[('True', 'Yes'), ('False', 'No')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )
    region = forms.ChoiceField(
        label="Région",
        choices=REGION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'region'}),
    )

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise ValidationError("L'âge doit être supérieur ou égal à 18 ans.")
        return age

    def clean_bmi(self):
        bmi = self.cleaned_data.get('bmi')
        if bmi < 10 or bmi > 60:
            raise ValidationError("Le BMI doit être compris entre 10 et 60.")
        return bmi

    def clean_children(self):
        children = self.cleaned_data.get('children')
        if children < 0:
            raise ValidationError("Le nombre d'enfants ne peut pas être négatif.")
        return children
