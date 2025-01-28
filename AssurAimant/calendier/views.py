from django.shortcuts import render
from django import forms
from django.forms.fields import DateField
from django.forms import DateInput
from .models import Rendezvous

class DateInput(DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date = DateField(widget=DateInput)


def calendar_view(request):
    form = DateForm(request.POST)
    if form.is_valid():
        selected_date = form.cleaned_data['date']
        if selected_date.day == 28:
            user_rendezvous, created = Rendezvous.objects.get_or_create(
                    user = request.user,
                    )
            user_rendezvous.jour = selected_date.day
            user_rendezvous.mois = selected_date.month
            user_rendezvous.annee = selected_date.year
            user_rendezvous.save()

        else:
            print('no date available')

    return render(request, 'calendar.html', {'form': form})

