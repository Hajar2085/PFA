from django import forms
from .models import Matiere, Cours

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Nom de la discipline (ex: Mathématiques)'})
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['titre', 'matiere', 'fichier_pdf']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Ex: Chapitre 1: Introduction'}),
            'matiere': forms.Select(attrs={'class': 'form-select form-control-custom'}),
            'fichier_pdf': forms.FileInput(attrs={'class': 'form-control form-control-custom'})
        }
