import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Personnel

class FonctionCategoryFilter(admin.SimpleListFilter):
    title = 'Catégorie de fonction'  
    parameter_name = 'fonction_category'  

    def lookups(self, request, model_admin):
        return [
            ('medecins', 'Médecins'),
            ('infirmiers', 'Infirmiers'),
            ('techniciens', 'Techniciens'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'medecins':
            return queryset.filter(fonction__in=[
                'Médecin Generaliste', 'Médecin Cardiologue', 'Médecin Dermatologue', 'Médecin Pediatre', 
                'Médecin Chirurgien', 'Médecin Radiologue', 'Médecin Psychiatre', 'Médecin Gynecologue'
            ])
        if self.value() == 'infirmiers':
            return queryset.filter(fonction='Infirmier')
        if self.value() == 'techniciens':
            return queryset.filter(fonction='Technicien')
        return queryset

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'fonction', 'telephone', 'email', 'adresse', 'photo')
    search_fields = ('nom', 'prenom', 'fonction', 'email', 'telephone')
    list_filter = (FonctionCategoryFilter,)
    list_editable = ('fonction', 'telephone', 'adresse', 'photo')
    list_per_page = 20

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'fonction', 'telephone', 'email', 'photo'),
        }),
        ('Détails supplémentaires', {
            'fields': ('adresse',),
            'classes': ('collapse',),
        }),
    )

    # Action pour générer le CSV
    def export_as_csv(self, request, queryset):
        # Création de la réponse HTTP avec un type MIME CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="personnel.csv"'
        
        # Création de l'objet CSV
        writer = csv.writer(response)
        writer.writerow(['Nom', 'Prénom', 'Fonction', 'Téléphone', 'Email', 'Adresse'])  # En-têtes du CSV
        
        # Écriture des données du queryset dans le CSV
        for personnel in queryset:
            writer.writerow([personnel.nom, personnel.prenom, personnel.fonction, personnel.telephone, personnel.email, personnel.adresse])
        
        return response
    
    # Définir l'action dans l'admin
    export_as_csv.short_description = "Exporter en CSV"
    actions = [export_as_csv]  # Ajout de l'action à la liste des actions disponibles

admin.site.register(Personnel, PersonnelAdmin)
