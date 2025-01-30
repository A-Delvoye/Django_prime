from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from .views import developer_dashboard, prediction_page, prediction_history

"""
    urlpatterns : URLs of the application
"""
urlpatterns = [
    path('', views.profileprediction, name='profileprediction'),
    path('prediction/', prediction_page, name='prediction_page'),
    path('prediction/history/', prediction_history, name='prediction_history'),
    path('prediction/dashboard/', developer_dashboard, name='developer_dashboard'),
]