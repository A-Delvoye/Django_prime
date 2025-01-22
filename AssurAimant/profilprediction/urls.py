from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
urlpatterns = [
    #path('profilprediction/login/', auth_views.LoginView.as_view(template_name='profilprediction/login.html'), name='login'),
    path('p/', views.profileprediction, name='profile2'),
    path('', RedirectView.as_view(url="profilprediction/test.html")),
    path('connexion', views.CustomConnexion.as_view(), name="connexion"),
]