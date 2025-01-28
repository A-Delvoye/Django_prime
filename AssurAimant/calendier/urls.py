from django.urls import path
from calendier import views
from .views import calendar_view


urlpatterns = [
    path("", views.calendar_view, name="calendar"),
    
]