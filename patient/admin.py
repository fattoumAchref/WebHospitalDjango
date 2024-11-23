from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_active')

    # Champs pour la recherche
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    # Filtres disponibles dans la barre latérale
    list_filter = ('is_active',)

    # Champs éditables directement dans la liste
    list_editable = ('phone_number', 'is_active')

    # Organisation des sections dans les formulaires d’ajout/modification
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('username', 'password'),
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number'),
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # Champs affichés dans le formulaire d'ajout d'utilisateur
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_active'),
        }),
    )

    # Pagination dans la liste des utilisateurs
    list_per_page = 20

# Enregistrer le modèle dans l’administration avec la configuration personnalisée
admin.site.register(CustomUser, CustomUserAdmin)
