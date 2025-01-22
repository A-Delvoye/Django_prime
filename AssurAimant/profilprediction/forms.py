from django import forms
from .models import ProfilePrediction
from django import forms

class ProfilePredictionForm(forms.Form):


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

    #age = forms.IntegerField()
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = forms.IntegerField()
    sex = forms.CharField()
    bmi = forms.FloatField()
    children = forms.IntegerField()
    smoker = forms.BooleanField()
    region = forms.ChoiceField(choices=REGION_CHOICES)
   # profile_updated_at = forms.DateTimeField()

    class Meta:
        #model = ProfilePrediction
        fields = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control'}),
            'children': forms.NumberInput(attrs={'class': 'form-control'}),
            'smoker': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
        }