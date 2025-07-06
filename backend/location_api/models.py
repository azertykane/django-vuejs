from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL   # "comptes.Utilisateur"

class Maison(models.Model):
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maisons")
    adresse      = models.CharField(max_length=255)
    latitude     = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description  = models.TextField(blank=True)
    cree_le      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maison #{self.id} – {self.adresse}"

class Chambre(models.Model):
    maison        = models.ForeignKey(Maison, on_delete=models.CASCADE, related_name="chambres")
    titre         = models.CharField(max_length=255)
    description   = models.TextField(blank=True)
    taille        = models.CharField(max_length=50)           # ex : 12m²
    type          = models.CharField(max_length=50, choices=[
        ("simple", "Chambre simple"), ("appartement", "Appartement"),
        ("maison", "Maison complète"),
    ])
    meublee       = models.BooleanField(default=False)
    salle_de_bain = models.BooleanField(default=False)
    prix          = models.DecimalField(max_digits=10, decimal_places=2)
    disponible    = models.BooleanField(default=True)
    cree_le       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Contrat(models.Model):
    locataire       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contrats")
    chambre         = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name="contrats")
    date_debut      = models.DateField()
    date_fin        = models.DateField(null=True, blank=True)
    montant_caution = models.DecimalField(max_digits=10, decimal_places=2)
    mois_caution    = models.PositiveSmallIntegerField()
    description     = models.TextField(blank=True)
    mode_paiement   = models.CharField(max_length=50, choices=[
        ("virement", "Virement"), ("cash", "Cash"), ("mobile_money", "Mobile money"),
    ])
    periodicite     = models.CharField(max_length=20, choices=[
        ("journalier", "Journalier"), ("hebdomadaire", "Hebdomadaire"), ("mensuel", "Mensuel"),
    ], default="mensuel")
    statut          = models.CharField(max_length=20, choices=[
        ("actif", "Actif"), ("resilie", "Résilié"),
    ], default="actif")
    cree_le         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrat #{self.id} – {self.chambre}"

class Paiement(models.Model):
    contrat        = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name="paiements")
    montant        = models.DecimalField(max_digits=10, decimal_places=2)
    statut         = models.CharField(max_length=20, choices=[("paye", "Payé"), ("impaye", "Impayé")])
    date_echeance  = models.DateField()
    date_paiement  = models.DateTimeField(null=True, blank=True)
    cree_le        = models.DateTimeField(auto_now_add=True)

class RendezVous(models.Model):
    locataire  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rendezvous")
    chambre    = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name="rendezvous")
    date_heure = models.DateTimeField()
    statut     = models.CharField(max_length=20, choices=[
        ("en_attente", "En attente"), ("confirme", "Confirmé"), ("annule", "Annulé"),
    ], default="en_attente")
    cree_le    = models.DateTimeField(auto_now_add=True)

# location_api/models.py
class Media(models.Model):
    maison  = models.ForeignKey(
        Maison, on_delete=models.CASCADE,
        related_name="medias", null=True, blank=True
    )
    chambre = models.ForeignKey(
        Chambre, on_delete=models.CASCADE,
        related_name="medias", null=True, blank=True
    )
    fichier     = models.FileField(upload_to="medias/")
    type        = models.CharField(max_length=10, choices=[("photo", "Photo"), ("video", "Vidéo")])
    description = models.TextField(blank=True)
    cree_le     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media #{self.id}"


class Probleme(models.Model):
    contrat     = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name="problemes")
    signale_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    type        = models.CharField(max_length=20, choices=[
        ("plomberie", "Plomberie"), ("electricite", "Électricité"), ("autre", "Autre"),
    ])
    responsable = models.CharField(max_length=20, choices=[
        ("locataire", "Locataire"), ("proprietaire", "Propriétaire"),
    ])
    resolu      = models.BooleanField(default=False)
    cree_le     = models.DateTimeField(auto_now_add=True)
