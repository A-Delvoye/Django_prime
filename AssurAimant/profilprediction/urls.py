from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from .views import prediction_page, prediction_history

urlpatterns = [
    path('', views.profileprediction, name='profileprediction'),
    path('prediction/', prediction_page, name='prediction_page'),
    path('prediction/history/', prediction_history, name='prediction_history'),
    #path('connexion', views.CustomConnexion.as_view(), name="connexion"),
]