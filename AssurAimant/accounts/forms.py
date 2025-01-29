from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
        UserCreationForm (_type_): a form to create a new user
    """
    email = forms.EmailField(required=True, label="Adresse e-mail")
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom de famille")
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nom d’utilisateur',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Adresse e-mail',
                'class': 'form-input'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Prénom',
                'class': 'form-input'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Nom de famille',
                'class': 'form-input'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Mot de passe',
                'class': 'form-input'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirmez le mot de passe',
                'class': 'form-input'
            }),}
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, commit=True):
        """Sauvegarde de l'utilisateur avec les données supplémentaires."""
        user = super().save(commit=True)  # Ne sauvegarde pas encore l'utilisateur
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user