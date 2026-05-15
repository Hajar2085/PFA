from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_professeur = models.BooleanField(default=False)
    is_etudiant = models.BooleanField(default=False)

class Matiere(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Cours(models.Model):
    titre = models.CharField(max_length=255)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='cours')
    fichier_pdf = models.FileField(upload_to='cours/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    texte = models.TextField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentaires')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.cours.titre}"

class Progression(models.Model):
    etudiant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progressions')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='progressions')
    est_termine = models.BooleanField(default=False)

    class Meta:
        unique_together = ('etudiant', 'cours')

    def __str__(self):
        return f"Progression de {self.etudiant.username} sur {self.cours.titre}"


class Video(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='videos')
    titre = models.CharField(max_length=255)
    youtube_url = models.URLField()
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('matiere', 'youtube_url')

    def __str__(self):
        return f"{self.titre} ({self.matiere.nom})"
