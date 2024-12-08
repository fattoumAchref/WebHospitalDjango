from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ForgotPasswordForm
from .forms import PatientUpdateForm
from django.contrib.auth.decorators import login_required
from personnel.models import Personnel
from django.conf import settings
from patient.models import CustomUser  # Import de ton modèle personnalisé


# Inscription
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Connexion
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue ! Vous êtes maintenant connecté.')
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Erreur lors de la saisie. Veuillez réessayer.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Page d'accueil
def home(request):
    doctors = Personnel.objects.filter(fonction__startswith="Médecin")
    return render(request, 'index.html', {'doctors': doctors})

# Mise à jour du profil utilisateur (Patient)
@login_required
def update_patient(request):
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont été mises à jour avec succès.")
            return redirect('update_patient')
    else:
        form = PatientUpdateForm(instance=request.user)
    return render(request, 'modif_patient.html', {'form': form})

# Suppression du compte utilisateur
@login_required
def delete_patient(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès.")
        return redirect('home')
    return render(request, 'delete_patient.html')

# Demande de réinitialisation de mot de passe
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)

            if users.exists():
                for user in users:
                    # Générer un token sécurisé et un lien de réinitialisation
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(str(user.pk).encode())

                    # Utiliser reverse pour générer l'URL
                    reset_url = request.build_absolute_uri(reverse('reset_password', args=[uid, token]))

                    # Envoyer l'e-mail
                    try:
                        send_mail(
                            'Réinitialisation de mot de passe',
                            f'Bonjour, cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_url}',
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email],
                            fail_silently=False
                        )
                        messages.success(request, "Si cet e-mail est enregistré, un lien de réinitialisation a été envoyé.")
                    except Exception as e:
                        messages.error(request, f"Erreur lors de l'envoi de l'e-mail : {e}")
            else:
                messages.error(request, "Aucun utilisateur avec cet e-mail n'a été trouvé.")
            return redirect('login')  # Redirection après soumission
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})

# Réinitialisation de mot de passe
def reset_password(request, uidb64, token):
    try:
        # Décoder l'UID pour récupérer l'utilisateur
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)  # Remplacer User par CustomUser

        # Vérifier la validité du token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
                    return redirect('login')  # Rediriger vers la page de connexion
            else:
                form = SetPasswordForm(user)
            return render(request, 'reset_password.html', {'form': form})
        else:
            return HttpResponse('Le lien est invalide ou a expiré.', status=400)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return HttpResponse('Lien invalide.', status=400)
