from django.contrib import admin
from .models import Jeune


@admin.register(Jeune)
class JeuneAdmin(admin.ModelAdmin):
    """Configuration d'administration pour le modèle Jeune"""
    
    list_display = ('matricule', 'prenom', 'nom', 'age', 'genre', 'telephone', 'zone')
    list_filter = ('genre', 'Domaine_activite', 'Niveau_etude', 'zone')
    search_fields = ('nom', 'prenom', 'numero_cni', 'matricule', 'email', 'telephone')
    ordering = ('-id',)
    
    fieldsets = (
        ('Informations Personnelles', {
            'fields': ('nom', 'prenom', 'age', 'genre', 'numero_cni', 'matricule')
        }),
        ('Adresse et Contact', {
            'fields': ('zone', 'adresse', 'telephone', 'telephone2', 'email')
        }),
        ('Éducation et Compétences', {
            'fields': ('Domaine_activite', 'Niveau_etude', 'competences')
        }),
    )
    
    readonly_fields = ('matricule',)
    
    def get_readonly_fields(self, request, obj=None):
        # Rendre numero_cni en lecture seule si la personne existe déjà
        readonly = list(self.readonly_fields)
        if obj:
            readonly.append('numero_cni')
        return readonly