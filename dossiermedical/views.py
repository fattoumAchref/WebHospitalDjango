from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import DossierMedicalForm

# Vérifie si l'utilisateur est un admin
def est_admin(user):
    return user.is_staff  # Utilise `is_superuser` si tu veux que seuls les superadmins aient accès

@login_required
@user_passes_test(est_admin)
def ajouter_dossier_medical(request):
    if request.method == 'POST':
        form = DossierMedicalForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_dossiers_medicaux')  # Redirige vers une page où sont listés les dossiers médicaux
    else:
        form = DossierMedicalForm()
    return render(request, 'ajouter_dossier.html', {'form': form})
