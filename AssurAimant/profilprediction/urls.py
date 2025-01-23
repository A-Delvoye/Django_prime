from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
urlpatterns = [
    path('', views.profileprediction, name='profile2'),
    #path('connexion', views.CustomConnexion.as_view(), name="connexion"),
]