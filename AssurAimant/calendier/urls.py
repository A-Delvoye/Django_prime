from django.urls import path
from calendier import views
from .views import calendar_view


urlpatterns = [
    path("", views.calendar_view, name="calendar"),
    path('delete_rendezvous/<int:rendezvous_id>/', views.delete_rendezvous, name='delete_rendezvous'),
    
]