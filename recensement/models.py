from django.db import models

# Create your models here.

class Jeune(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    age = models.IntegerField()
    genre = models.CharField(max_length=10)
    zone = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    telephone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    Domaine_activite = models.CharField(max_length=100, null=True, blank=True)
    Niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    competences = models.TextField()
    numero_cni = models.CharField(max_length=50, unique=True)

    matricule = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nom + " " + self.prenom
    
    def save(self, *args, **kwargs):
        if not self.matricule:
            prefix = "J"
            if self.numero_cni and len(self.numero_cni) >= 4:
                unique_id = str(self.numero_cni).zfill(5)
            else:
                unique_id = str(self.id).zfill(5) if self.id else "00001"
            self.matricule = f"{prefix}{unique_id}"
        super().save(*args, **kwargs)
