# views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import FactureForm
from .models import Facture
# Vérifie si l'utilisateur est un admin
def est_admin(user):
    return user.is_staff

@login_required
@user_passes_test(est_admin)
def ajouter_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_list')  # Redirige vers une page listant toutes les factures
    else:
        form = FactureForm()
    return render(request, 'ajouter_facture.html', {'form': form})

@login_required
def facture_list(request):
    factures = Facture.objects.filter(patient=request.user)
    return render(request, 'factures_list.html', {'factures': factures})