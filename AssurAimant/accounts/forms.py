from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    # USER_TYPE_CHOICES = [
    #     ('client', 'Client'),
    #     ('developer', 'Développeur'),
    #     ('advisor', 'Conseiller'),
    # ]
    # user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')


    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        # user.user_type = self.cleaned_data["user_type"]  # Enregistrez le type utilisateur
        if commit:
            user.save()
        return user