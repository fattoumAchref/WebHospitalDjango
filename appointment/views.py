from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from .forms import AppointmentForm
from transformers import pipeline
from langdetect import detect
import re

# Check if user is an administrator
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirect to a page listing appointments
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Sauvegarder le rendez-vous
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Lier le rendez-vous à l'utilisateur connecté (patient)
            appointment.save()

            # Envoi de l'e-mail de confirmation
            subject = 'Confirmation de votre rendez-vous'
            message = f'Bonjour {request.user.first_name},\n\nVotre rendez-vous a été pris avec succès pour le {appointment.date}.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]  # L'email du patient qui a pris rendez-vous

            send_mail(subject, message, from_email, recipient_list)

            # Message de succès
            messages.success(request, "Votre rendez-vous a été pris avec succès.")
            return redirect('home')  # Ou redirigez où tu veux après succès
        else:
            messages.error(request, "Erreur lors de la prise de rendez-vous. Veuillez réessayer.")
    else:
        form = AppointmentForm()
    
    return render(request, 'make_appointment.html', {'form': form})

@login_required
def update_appointment(request, appointment_id):
    # Récupérer le rendez-vous associé à ce patient
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            # Sauvegarder les modifications du rendez-vous
            form.save()

            # Envoi de l'e-mail de confirmation après mise à jour
            subject = 'Votre rendez-vous a été modifié'
            message = f'Bonjour {request.user.first_name},\n\nVotre rendez-vous a été modifié avec succès pour le {appointment.date}.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]  # Email du patient

            send_mail(subject, message, from_email, recipient_list)

            # Message de succès
            messages.success(request, "Rendez-vous modifié avec succès.")
            return redirect('appointment_list')  # Redirige vers la liste des rendez-vous
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier les champs.")
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'update_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Le rendez-vous a été supprimé avec succès.")
    return redirect('list_appointments')  # Remplacez par le nom de votre vue de liste.

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def send_confirmation_email(request):
    # Contenu de l'e-mail
    subject = 'Confirmation de votre rendez-vous'
    message = 'Votre rendez-vous a été confirmé avec succès.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['destinataire@example.com']  # Liste des destinataires

    # Envoi de l'e-mail
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponse('E-mail envoyé avec succès !')

#sentiment analysis
class CommentaireAIService:
    def __init__(self):
        # Pipeline d'analyse de sentiment (avec prise en charge des sentiments neutres)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", 
            model="cardiffnlp/twitter-roberta-base-sentiment"
        )

        # Pipeline de traduction vers l'anglais
        self.translator_to_english = pipeline(
            "translation", 
            model="Helsinki-NLP/opus-mt-mul-en"  # Modèle multilingue -> anglais
        )
        
        # Modèle pour la détection des dialectes arabes
        self.dialect_identifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            tokenizer="facebook/bart-large-mnli"
        )
    
    def detecter_langue(self, commentaire):
        """
        Détecte la langue du commentaire en détectant les dialectes arabes et autres langues.
        """
        try:
            # Utiliser langdetect pour les langues courantes
            langue = detect(commentaire)
            
            # Si la langue détectée est l'arabe, on passe à une détection de dialecte plus précise
            if langue == 'ar':
                dialectes_possibles = ['ar-tun', 'ar-eg', 'ar-sa', 'ar-dz', 'ar-ma', 'ar-ly']
                # Utilisation d'un modèle pour identifier un dialecte spécifique
                result = self.dialect_identifier(commentaire, candidate_labels=dialectes_possibles)
                langue = result['labels'][0]  # Prendre le dialecte le plus probable
            
            return langue
        
        except Exception as e:
            print(f"Erreur de détection de langue: {e}")
            return 'error'

    def traduire_vers_anglais(self, commentaire):
        """
        Traduit le commentaire vers l'anglais si nécessaire.
        """
        try:
            result = self.translator_to_english(commentaire)
            return result[0]['translation_text']
        except Exception as e:
            print(f"Erreur de traduction: {e}")
            return commentaire  # Retourner le commentaire original en cas d'erreur de traduction
    
    def analyser_sentiment(self, commentaire):
        """
        Analyse le sentiment du commentaire en gérant plusieurs langues, avec prise en charge explicite des sentiments neutres.
        """
        try:
            # Étape 1: Détection de la langue
            langue = self.detecter_langue(commentaire)

            # Étape 2: Traduction si nécessaire
            if langue != 'en':  # Si la langue n'est pas l'anglais
                commentaire = self.traduire_vers_anglais(commentaire)

            # Étape 3: Analyse de sentiment
            result = self.sentiment_analyzer(commentaire)[0]

            # Mappage des labels en sentiments textuels
            sentiment_map = {
                'LABEL_0': 'NEGATIVE',
                'LABEL_1': 'NEUTRAL',
                'LABEL_2': 'POSITIVE'
            }

            # Récupération du sentiment et du score
            sentiment = sentiment_map.get(result['label'], 'NEUTRAL')  # Par défaut 'NEUTRAL' si le label n'est pas reconnu
            score = result['score']

            return {
                'langue_detectee': langue,
                'sentiment': sentiment,
                'score': score  # Confiance du modèle (0 à 1)
            }
        except Exception as e:
            print(f"Erreur d'analyse de sentiment: {e}")
            return {
                'langue_detectee': 'error',
                'sentiment': 'NEUTRAL',
                'score': 0.5  # Valeur par défaut pour l'erreur
            }

    def filtrer_commentaires_inappropries(self, commentaire):
        """
        Filtrer les commentaires contenant des mots inappropriés, y compris les insultes et vulgarités.
        """
        mots_interdits = [
            # Insultes générales (français)
            'idiot', 'stupide', 'imbécile', 'crétin', 'abruti', 'nul', 'minable', 'débile',
    
            # Insultes vulgaires (français)
            'con', 'connard', 'connasse', 'salaud', 'salopard', 'ordure', 'merde', 'chiant', 
            'pute', 'p***', 'prostituée', 'enculé', 'bordel',
    
            # Insultes racistes ou discriminatoires (français)
            'raciste', 'nègre', 'bougnoule', 'chintok', 'youpin', 'pédé', 'tapette', 
            'gouine', 'handicapé', 'mongolien', 'anormal', 'difforme',
    
            # Mots agressifs ou menaçants (français)
            'meurtre', 'assassiner', 'viol', 'tuer', 'détruire', 'attaquer', 'harceler', 
            'menace', 'casser',
    
            # Langage vulgaire ou à connotation sexuelle (français)
            'bite', 'sexe', 'baiser', 'cul', 'niquer', 'cochon', 'porno', 'pornographique', 
            'masturbation',
    
            # Expressions pour insulter ou rabaisser (français)
            'tu sers à rien', 'ferme-la', 'dégage', 'tais-toi', 't’es qu’une merde', 
            'je te hais', 'va te faire voir', 'casse-toi',
    
            # Variations orthographiques ou abrégées (français)
            'c*n', 'fdp', 'tg', 'ntm', 'prout', 'mdr t ki', 'kes tu veux', 'nique ta mère',
    
            # Insultes générales (anglais)
            'idiot', 'stupid', 'dumb', 'useless', 'loser', 'jerk', 'moron',
    
            # Insultes vulgaires (anglais)
            'shit', 'crap', 'bitch', 'bastard', 'asshole', 'freak', 'fuck', 'f***', 
            'motherfucker', 'slut', 'dick', 'whore',
    
            # Expressions haineuses ou offensantes (anglais)
            'kill', 'murder', 'rape', 'attack', 'harass', 'hate', 'destroy',
    
            # Expressions offensantes tunisiennes
            'tfo', 'aala khrek', 'aala omek', 'aala bok', 'ana nikk omek', 
            '7achetek', 'kosom omek',
        ]

        # Vérification des mots interdits insensibles à la casse
        commentaire_lower = commentaire.lower()

        # Utilisation de regex pour permettre les variations orthographiques et trouver des mots partiels
        for mot in mots_interdits:
            pattern = r'\b' + re.escape(mot) + r'\b'
            if re.search(pattern, commentaire_lower):
                return False  # Commentaire non approprié

        return True  # Commentaire approprié