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

# Enregistrement du modèle et de l'administration personnalisée
admin.site.register(Facture, FactureAdmin)
