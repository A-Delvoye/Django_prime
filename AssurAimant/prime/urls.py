from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
#from . import views
from .views import ma_vue

urlpatterns = [
    path('test', ma_vue, name="test"),
]