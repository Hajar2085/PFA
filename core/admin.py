from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Matiere, Cours, Commentaire, Progression

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Colonnes affichées dans la liste des utilisateurs
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_etudiant', 'is_professeur', 'is_staff']
    
    # Filtres sur le côté droit
    list_filter = ['is_etudiant', 'is_professeur', 'is_staff', 'is_superuser', 'is_active']
    
    # Barre de recherche
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    # Pour l'édition d'un utilisateur existant (ajout de nos champs personnalisés)
    fieldsets = UserAdmin.fieldsets + (
        ('Rôles Plateforme', {'fields': ('is_etudiant', 'is_professeur')}),
    )
    
    # Pour la création d'un NOUVEL utilisateur depuis l'interface admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôles Plateforme', {'fields': ('is_etudiant', 'is_professeur')}),
    )

class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'date_ajout', 'get_commentaires_count')
    list_filter = ('matiere', 'date_ajout')
    search_fields = ('titre', 'matiere__nom')
    date_hierarchy = 'date_ajout'
    
    def get_commentaires_count(self, obj):
        return obj.commentaires.count()
    get_commentaires_count.short_description = 'Nb de Commentaires'

class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'get_cours_count')
    search_fields = ('nom',)
    
    def get_cours_count(self, obj):
        return obj.cours.count()
    get_cours_count.short_description = 'Nb de Cours'

class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'cours', 'date_creation', 'apercu_texte')
    list_filter = ('cours', 'date_creation')
    search_fields = ('texte', 'auteur__username', 'cours__titre')
    
    def apercu_texte(self, obj):
        return obj.texte[:50] + '...' if len(obj.texte) > 50 else obj.texte
    apercu_texte.short_description = 'Texte'

class ProgressionAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'est_termine')
    list_filter = ('est_termine', 'cours', 'etudiant')
    search_fields = ('etudiant__username', 'cours__titre')

# Enregistrement des modèles
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Cours, CoursAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
admin.site.register(Progression, ProgressionAdmin)

# Pour changer le titre de l'interface d'administration
admin.site.site_header = "Administration ÉduPlateforme"
admin.site.site_title = "Admin ÉduPlateforme"
admin.site.index_title = "Gestion de la plateforme"
