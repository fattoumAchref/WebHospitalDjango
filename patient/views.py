from django.http import HttpResponse
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
from .predictions import train_model_with_cross_validation
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from sklearn.metrics import roc_curve, auc
import csv
import pandas as pd


# Inscription

from django.contrib.admin.views.decorators import staff_member_required

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
            messages.success(request, "Vos informations ont étées mises à jour avec succès.")
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
@staff_member_required
def custom_dashboard(request):
    return HttpResponse("<h1>Welcome to the Custom Dashboard</h1>")

@login_required
def model_results_view(request):
    if request.method == 'POST':
        # Entraîner le modèle et obtenir les métriques et prédictions
        model, mean_accuracy, f1, roc_auc, X_test, y_test, y_pred_proba = train_model_with_cross_validation()

        # Chargement des données des patients
        patients = CustomUser.objects.all()
        data = [{'age': p.age, 'imc': p.imc} for p in patients if p.taille and p.poids]
        df = pd.DataFrame(data)

        # Récupérer un patient par défaut (ou connecté via un formulaire, par exemple)
        patient_id = request.POST.get('patient_id')
        #connected_patient = CustomUser.objects.filter(id=patient_id).first()
        connected_patient = request.user

        patient_message = ""
        patient_recommendation = ""


        print(f"Patient trouvé : {connected_patient}")

        if connected_patient and connected_patient.taille and connected_patient.poids:
            # Calculer les caractéristiques du patient sélectionné
            patient_data = {
                'age': connected_patient.age,
                'gender': {'Male': 0, 'Female': 1}.get(connected_patient.gender, 2),
                'poids': connected_patient.poids,
                'taille': connected_patient.taille,
                'imc': connected_patient.imc,
            }
            # Convertir en DataFrame pour prédiction
            patient_df = pd.DataFrame([patient_data])
            prob_readmission = model.predict_proba(patient_df)[0][1]  # Probabilité de réadmission
            patient_message = f"Votre probabilité de réadmission est de {prob_readmission:.2%}."

            # Ajouter des recommandations
            if prob_readmission <= 0.30:
                patient_recommendation = "Votre risque de réadmission est faible. Continuez à suivre vos soins habituels."
            elif prob_readmission <= 0.60:
                patient_recommendation = "Votre risque de réadmission est modéré. Pensez à planifier une visite de contrôle."
            else:
                patient_recommendation = "Votre risque de réadmission est élevé. Veuillez consulter un médecin dès que possible."
        else:
            patient_message = "Impossible de calculer votre risque de réadmission : données insuffisantes."

        # Génération de l'histogramme des âges
        plt.figure(figsize=(6, 4))
        plt.hist(df['age'], bins=10, color='skyblue', edgecolor='black')
        plt.title('Répartition des âges')
        plt.xlabel('Âge')
        plt.ylabel('Nombre de patients')
        buffer_age = BytesIO()
        plt.savefig(buffer_age, format='png')
        buffer_age.seek(0)
        graphic_age = base64.b64encode(buffer_age.getvalue()).decode('utf-8')
        buffer_age.close()

        # Génération de la courbe ROC
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc_value = auc(fpr, tpr)

        plt.figure(figsize=(6, 4))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc_value:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.title('Receiver Operating Characteristic')
        plt.xlabel('Taux de faux positifs')
        plt.ylabel('Taux de vrais positifs')
        plt.legend(loc='lower right')
        buffer_roc = BytesIO()
        plt.savefig(buffer_roc, format='png')
        buffer_roc.seek(0)
        graphic_roc = base64.b64encode(buffer_roc.getvalue()).decode('utf-8')
        buffer_roc.close()

        # Ajout des graphiques et des métriques au contexte
        context = {
            'mean_accuracy': round(mean_accuracy * 100, 2),
            'f1_score': round(f1, 2),
            'roc_auc': round(roc_auc, 2),
            'message': "Le modèle a été entraîné avec succès !",
            'graphic_age': graphic_age,
            'graphic_roc': graphic_roc,
            'patient_message': patient_message,  # Message personnalisé
            'patient_recommendation': patient_recommendation,  # Recommandation personnalisée
            'patients': patients,  # Pour afficher tous les patients dans la vue
        }
    else:
        # Afficher une page de démarrage
        context = {
            'message': "Cliquez sur le bouton pour entraîner le modèle.",
            'patients': CustomUser.objects.all(),  # Inclure les patients pour sélection
        }

    return render(request, 'model_results.html', context)

def download_report(request):
    # Préparer une réponse HTTP pour un fichier CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)

    # Ajouter un en-tête au fichier CSV
    writer.writerow(['Numero ID', 'Nom', 'Prenom', 'Age', 'gender', 'IMC', 'Performance'])

    # Récupérer les patients pour inclure dans le rapport
    patients = CustomUser.objects.all()

    # Ajoute les performances du modèle si pertinent
    try:
        model, mean_accuracy, f1, roc_auc = train_model_with_cross_validation()
        writer.writerow([])
        writer.writerow(['Performance du modele'])
        writer.writerow(['Precision moyenne (%)', round(mean_accuracy * 100, 2)])
        writer.writerow(['F1 Score', round(f1, 2)])
        writer.writerow(['ROC-AUC Score', round(roc_auc, 2)])
        writer.writerow([])
    except Exception as e:
        writer.writerow([])
        writer.writerow(['Erreur lors de lentraînement du modele'])
        writer.writerow([str(e)])
        writer.writerow([])

    # Ajouter les détails des patients
    for patient in patients:
        gender = patient.gender
        imc = patient.imc if patient.imc else "N/A"
        writer.writerow([
            patient.last_name,
            patient.first_name,
            patient.age,
            gender,
            imc,
            'Donnees incluses'
        ])

    return response