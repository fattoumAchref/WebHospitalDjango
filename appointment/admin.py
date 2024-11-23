from django.contrib import admin
from django.utils.timezone import now
from django.contrib.admin import SimpleListFilter
from .models import Appointment
from datetime import timedelta
from django.core.mail import send_mail

# Créer un filtre personnalisé pour la date
class DateRangeFilter(SimpleListFilter):
    title = 'Date Range'  # Titre du filtre
    parameter_name = 'date_range'  # Nom du paramètre dans l'URL

    def lookups(self, request, model_admin):
        # Retourner les options de filtre disponibles
        return (
            ('today', 'Today'),
            ('last_7_days', 'Last 7 Days'),
            ('this_month', 'This Month'),
            ('this_year', 'This Year'),
        )

    def queryset(self, request, queryset):
        # Appliquer les filtres en fonction de la sélection
        value = self.value()
        today = now().date()
        
        if value == 'today':
            return queryset.filter(date=today)
        if value == 'last_7_days':
            return queryset.filter(date__gte=today - timedelta(days=7))
        if value == 'this_month':
            return queryset.filter(date__month=today.month, date__year=today.year)
        if value == 'this_year':
            return queryset.filter(date__year=today.year)
        return queryset


def send_confirmation_email(modeladmin, request, queryset):
    # Pour chaque rendez-vous sélectionné, envoyer un e-mail
    for appointment in queryset:
        send_mail(
            'Confirmation de votre rendez-vous',
            f'Cher(e) {appointment.patient.username},\n\nVotre rendez-vous avec {appointment.personnel.nom if appointment.personnel else "un membre du personnel"} est confirmé pour le {appointment.date} à {appointment.time}.\n\nMerci de votre confiance!',
            'salimmnif123@gmail.com',  # Remplacez avec l'adresse e-mail de l'expéditeur
            [appointment.patient.email],  # L'adresse e-mail du patient
            fail_silently=False,
        )
    modeladmin.message_user(request, "Les e-mails de confirmation ont été envoyés avec succès.")

# Ajouter cette action à l'administration de Appointment
send_confirmation_email.short_description = 'Envoyer un e-mail de confirmation'

# Admin personnalisé pour Appointment
class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ['patient__username', 'personnel__nom', 'date']
    list_filter = ['personnel', DateRangeFilter]  # Ajouter le filtre personnalisé ici
    list_display = ('patient', 'personnel', 'date', 'time', 'description')  # Afficher plus de champs dans la liste
    actions = [send_confirmation_email]  # Ajouter l'action pour envoyer des e-mails

# Enregistrer le modèle avec l'admin personnalisé
admin.site.register(Appointment, AppointmentAdmin)
