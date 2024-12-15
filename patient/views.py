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

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import cv2
import numpy as np
import face_recognition
import logging


# Inscription
# Fonction pour extraire les embeddings faciaux
def extract_face_embeddings(image_path):
    img = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(img)
    if face_encodings:
        return face_encodings[0]
    return None

# Fonction de similarité cosinus
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
def register(request):
    if request.method == 'POST':
        # Créer un formulaire avec les données POST et les fichiers
        form = CustomUserCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Récupérer les données du formulaire
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data.get('phone_number')
            face_image = form.cleaned_data.get('face_image')
            password = form.cleaned_data['password1']  # Récupérer le mot de passe

            # Créer un nouvel utilisateur avec CustomUser
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone_number
            )

            # Traitement de l'image faciale si elle est fournie
            if face_image:
                # Charger l'image faciale et récupérer les embeddings
                image = face_recognition.load_image_file(face_image)
                face_encoding = face_recognition.face_encodings(image)

                if len(face_encoding) == 0:
                    return JsonResponse({'status': 'error', 'message': 'Aucun visage détecté dans l\'image.'})

                # Convertir l'ndarray en liste et assigner les embeddings
                user.set_face_embeddings(face_encoding[0])  # On suppose que face_encoding[0] est un ndarray

            # Sauvegarder l'utilisateur avec les embeddings faciaux
            user.save()

            # Rediriger vers une autre page après l'inscription réussie
            return JsonResponse({'status': 'success', 'message': 'Utilisateur enregistré avec succès.'})

        # Si le formulaire n'est pas valide, retourner un message d'erreur
        return JsonResponse({'status': 'error', 'message': 'Les informations soumises sont invalides.'})

    # Si la méthode n'est pas POST, afficher le formulaire d'inscription
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
@login_required
def upload_face(request):
    if request.method == 'POST' and 'face_image' in request.FILES:
        user = request.user
        face_image = request.FILES['face_image']

        # Enregistrer l'image
        media_path = os.path.join(settings.MEDIA_ROOT, 'users', str(user.id))
        os.makedirs(media_path, exist_ok=True)
        image_path = os.path.join(media_path, 'face.jpg')
        with open(image_path, 'wb') as f:
            for chunk in face_image.chunks():
                f.write(chunk)

        # Extraire les embeddings de l'image (dummy embeddings pour exemple)
        embeddings = extract_face_embeddings(image_path)
        user.face_embeddings = embeddings
        user.save()

        messages.success(request, "Votre photo a été téléchargée avec succès.")
        return redirect('profile')
    return render(request, 'upload_face.html')

# Fonction d'extraction des embeddings (exemple simplifié)

# Tester avec une image spécifique

# Authentification par reconnaissance faciale
@csrf_exempt
def face_login(request):
    if request.method == 'POST':
        face_image = request.FILES['face_image']  # L'image envoyée depuis la vue frontend
        
        # Charger l'image et obtenir les embeddings
        image = face_recognition.load_image_file(face_image)
        face_encoding = face_recognition.face_encodings(image)
        
        if len(face_encoding) == 0:
            return JsonResponse({'status': 'error', 'message': 'Aucun visage détecté.'})
        
        uploaded_embedding = face_encoding[0]  # Embedding du visage envoyé
        
        # Comparer avec les embeddings des utilisateurs
        users = CustomUser.objects.exclude(face_embeddings__isnull=True)
        for user in users:
            known_embedding = np.array(user.face_embeddings)  # Embedding de l'utilisateur stocké
            distance = np.linalg.norm(uploaded_embedding - known_embedding)
            
            if distance < 0.6:  # Seuil de similarité
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Connexion réussie.'})
        
        return JsonResponse({'status': 'error', 'message': 'Aucune correspondance trouvée.'})


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

def custom_dashboard(request):
    return render(request, 'admin/custom_dashboard.html')  # Template for the dashboard 