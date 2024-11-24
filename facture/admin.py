import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Facture

class FactureAdmin(admin.ModelAdmin):
    # Champs affichés dans la liste des factures
    list_display = ('id', 'patient', 'montant', 'date_emission', 'date_paiement', 'est_payee')

    # Champs pour la recherche
    search_fields = ('patient__username', 'description')

    # Filtres dans la barre latérale
    list_filter = ('est_payee', 'date_emission', 'date_paiement')

    # Champs éditables directement dans la liste
    list_editable = ('est_payee', 'date_paiement')

    # Pagination dans la liste des factures
    list_per_page = 20

    # Organisation des champs dans le formulaire d’ajout/modification
    fieldsets = (
        ('Informations Générales', {
            'fields': ('patient', 'description', 'montant', 'est_payee'),
        }),
        ('Dates', {
            'fields': ('date_emission', 'date_paiement'),
        }),
    )

    # Lecture seule pour les champs automatiquement définis
    readonly_fields = ('date_emission',)

    # Action pour générer le CSV
    def export_as_csv(self, request, queryset):
        # Création de la réponse HTTP avec un type MIME CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="factures.csv"'
        
        # Création de l'objet CSV
        writer = csv.writer(response)
        writer.writerow(['ID', 'Patient', 'Description', 'Montant', 'Date Emission', 'Date Paiement', 'Est Payée'])  # En-têtes du CSV
        
        # Écriture des données du queryset dans le CSV
        for facture in queryset:
            writer.writerow([facture.id, facture.patient.username, facture.description, facture.montant, facture.date_emission, facture.date_paiement, facture.est_payee])
        
        return response
    
    # Définir l'action dans l'admin
    export_as_csv.short_description = "Exporter en CSV"
    actions = [export_as_csv]  # Ajout de l'action à la liste des actions disponibles

# Enregistrement du modèle et de l'administration personnalisée
admin.site.register(Facture, FactureAdmin)
