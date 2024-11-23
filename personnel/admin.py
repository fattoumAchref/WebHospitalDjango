from django.contrib import admin
from .models import Personnel
class FonctionCategoryFilter(admin.SimpleListFilter):
    title = 'Catégorie de fonction'  # Titre du filtre dans l'admin
    parameter_name = 'fonction_category'  # Nom du paramètre dans l'URL

    def lookups(self, request, model_admin):
        # Options affichées dans le filtre
        return [
            ('medecins', 'Médecins'),
            ('infirmiers', 'Infirmiers'),
            ('techniciens', 'Techniciens'),
        ]

    def queryset(self, request, queryset):
        # Filtrer les résultats selon la catégorie sélectionnée
        if self.value() == 'medecins':
            return queryset.filter(fonction__in=[
                'Generaliste', 'Cardiologue', 'Dermatologue', 'Pediatre', 
                'Chirurgien', 'Radiologue', 'Psychiatre', 'Gynecologue'
            ])
        if self.value() == 'infirmiers':
            return queryset.filter(fonction='Infirmier')
        if self.value() == 'techniciens':
            return queryset.filter(fonction='Technicien')
        return queryset  # Aucun filtre sélectionné, retourne tous les objets


class PersonnelAdmin(admin.ModelAdmin):
    # Champs à afficher dans la liste
    list_display = ('prenom', 'nom', 'fonction', 'telephone', 'email', 'adresse')

    # Ajout d'une barre de recherche
    search_fields = ('nom', 'prenom', 'fonction', 'email', 'telephone')

    # Filtres pour simplifier la navigation
    list_filter = (FonctionCategoryFilter,)

    # Champs à éditer directement dans la liste
    list_editable = ('fonction', 'telephone', 'adresse')

    # Pagination pour éviter de surcharger la liste
    list_per_page = 20

    # Organisation des champs dans le formulaire d'ajout/édition
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'fonction', 'telephone', 'email'),
        }),
        ('Détails supplémentaires', {
            'fields': ('adresse',),
            'classes': ('collapse',),  # Replié par défaut
        }),
    )

    

admin.site.register(Personnel,PersonnelAdmin)