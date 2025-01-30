from django.shortcuts import render, redirect
from django import forms
from .models import Rendezvous, User

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.Form):
    date = forms.DateField(widget=DateInput)

def calendar_view(request):
    form = DateForm(request.POST or None)
    
    if form.is_valid():
        print("0")
        selected_date = form.cleaned_data['date']
        day = selected_date.day
        month = selected_date.month
        year = selected_date.year
        
        # Récupérer le premier conseiller disponible (user avec is_staff=True)
        conseiller = User.objects.filter(is_staff=True).first()  # Récupère le premier conseiller disponible

        if conseiller:
            # Filtrer les rendez-vous pour cet utilisateur à la date donnée
            user_rendezvous = Rendezvous.objects.filter(
                user=request.user, 
                jour=day, 
                mois=month, 
                annee=year
            ).first()  # On prend seulement le premier rendez-vous trouvé (si plusieurs existent)
            
            if user_rendezvous:

                # Si un rendez-vous existe déjà, on met à jour le conseiller
                user_rendezvous.conseiller = conseiller
                user_rendezvous.save()  # Sauvegarder les modifications
            else:

                # Si aucun rendez-vous n'existe pour cet utilisateur à cette date, on crée un nouveau
                user_rendezvous = Rendezvous.objects.create(
                    user=request.user,
                    conseiller=conseiller,
                    jour=day,
                    mois=month,
                    annee=year
                )
            
            return redirect('calendar')  # Rediriger vers la même page après la soumission
            
        else:
            # Si aucun conseiller n'est trouvé, afficher un message d'erreur
            print('Aucun conseiller disponible pour ce rendez-vous.')
    
    # Afficher la vue avec le formulaire et les rendez-vous existants
    rendezvous_list = Rendezvous.objects.filter(user=request.user)
    return render(request, 'calendar.html', {'form': form, 'rendezvous_list': rendezvous_list})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Rendezvous

def delete_rendezvous(request, rendezvous_id):
    # Récupérer l'objet Rendezvous par son ID
    rendezvous = get_object_or_404(Rendezvous, id=rendezvous_id)
    
    # Vérifier que l'utilisateur est bien celui qui a créé le rendez-vous ou est un administrateur
    if rendezvous.user == request.user or request.user.is_staff:
        # Supprimer le rendez-vous
        rendezvous.delete()
        return redirect('calendar')  # Rediriger vers la page du calendrier après suppression
    else:
        # Si l'utilisateur n'a pas les droits, on peut afficher un message d'erreur
        return render(request, 'calendar.html', {'error': "Vous ne pouvez pas supprimer ce rendez-vous."})
