from django.contrib import admin
from .models import DossierMedical

class DossierMedicalAdmin(admin.ModelAdmin):
    # Champs affichés dans la liste
    list_display = ('id', 'patient', 'date_creation', 'dernier_mise_a_jour', 'description_excerpt','fichier')

    # Champs pour la recherche
    search_fields = ('patient__username', 'description')

    # Filtres pour la navigation
    list_filter = ('date_creation', 'dernier_mise_a_jour')

    # Pagination pour éviter de surcharger la liste
    list_per_page = 20

    # Organisation des champs dans le formulaire d’ajout/modification
    fieldsets = (
        ('Informations Patient', {
            'fields': ('patient',),
        }),
        ('Détails du Dossier Médical', {
            'fields': ('description','fichier'),
        }),
        ('Dates', {
            'fields': ('date_creation', 'dernier_mise_a_jour'),
        }),
    )

    # Champs en lecture seule
    readonly_fields = ('date_creation', 'dernier_mise_a_jour')

    def description_excerpt(self, obj):
        # Limite la description affichée dans la liste
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description

    description_excerpt.short_description = "Aperçu de la description"

# Enregistrement du modèle et de l'administration personnalisée
admin.site.register(DossierMedical, DossierMedicalAdmin)
