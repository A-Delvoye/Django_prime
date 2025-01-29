from django.shortcuts import render
from django import forms
from django.forms.fields import DateField
from django.forms import DateInput
from .models import Rendezvous, User

class DateInput(DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date = DateField(widget=DateInput)


def calendar_view(request):
    form = DateForm(request.POST)
    if form.is_valid():
        selected_date = form.cleaned_data['date']
        day = selected_date.day
        month = selected_date.month
        year = selected_date.year
        list_consultant = User.objects.filter(is_conseiller=1)
        not_available = Rendezvous.objects.filter(jour=day, mois=month, annee=year).values_list(conseiller)
        person_disp = set(list_consultant) - set(not_available)
        if person_disp != {}:
            user_rendezvous= Rendezvous.objects.get(user = request.user)
            user_rendezvous.conseiller= list(person_disp[0])
            user_rendezvous.jour = day
            user_rendezvous.mois = month
            user_rendezvous.annee = year
            user_rendezvous.save()
        else:
            print('no date available')

    return render(request, 'calendar.html', {'form': form})

