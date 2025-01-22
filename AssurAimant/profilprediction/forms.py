from django import forms
from .models import ProfilePrediction


class ProfilePredictionForm(forms.ModelForm):
    class Meta:
        model = ProfilePrediction
        fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control'}),
            'children': forms.NumberInput(attrs={'class': 'form-control'}),
            'smoker': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
        }