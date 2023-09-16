from django.db import models
from .models import *
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Patient(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    SEXE_CHOICES = (
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('autres', 'Autres'),
    )
    sexe = models.CharField(max_length=6, choices=SEXE_CHOICES)
    numero_dossier = models.CharField(max_length=15)
    date_de_naissance = models.DateField(default=timezone.now)  # Utilisez "null=True" pour autoriser les valeurs nulles.
    profession = models.CharField(max_length=25)
    adresse = models.CharField(max_length=25)
    telephone = models.CharField(max_length=15)  # Utilisez un champ de type "CharField" pour les numéros de téléphone.
    ASSURANCE_CHOICES = (
        ('oui', 'Oui'),
        ('non', 'Non'),
    )
    assurance = models.CharField(max_length=3, choices=ASSURANCE_CHOICES)  # Utilisez un champ de type "CharField" pour les choix.
    date = models.DateTimeField(default=timezone.now) # Vous devez ajouter "auto_now_add=True" si c'est un champ de date automatiquement généré.
    def __str__(self):
        return f"{self.prenom} {self.nom} - Dossier: {self.numero_dossier}"



class SalleDAttente(models.Model):
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    numero_dossier = models.CharField(max_length=8)
    heure_arrivee = models.DateTimeField(default=timezone.now)
    TRAITEMENT_CHOICES = (
        ('laser', 'Laser'),
        ('consultation', 'Consultation'),
        ('examen', 'Examen'),
        ('operation', 'Operation'),
        ('lunette', 'Lunette'),
        ('piqure', 'Piqure'),
    )
    traitement = models.CharField(max_length=25,choices=TRAITEMENT_CHOICES )

    def __str__(self):
        return f"{self.nom} {self.prenom} - Dossier: {self.numero_dossier}"




class Vision(models.Model):
    patient = models.ForeignKey(SalleDAttente, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    cylindre_os = models.FloatField()
    cylindre_od = models.FloatField()
    sphere_od = models.FloatField()
    sphere_os = models.FloatField()
    axe_od = models.IntegerField()
    axe_os = models.IntegerField()
    tension_od = models.FloatField()
    tension_os = models.FloatField()
    vision_os = models.CharField(max_length=100)
    vision_od = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.patient.prenom} {self.patient.nom}"



class MedecinOphalmo(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=200)
    numero_telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.specialite}"



class Consultation(models.Model):
    patient = models.ForeignKey(Vision, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    medecin = models.ForeignKey(MedecinOphalmo, on_delete=models.CASCADE)
    debut = models.DateTimeField(default=timezone.now)
    motif_consultation = models.CharField(max_length=50)
    avis = models.CharField(max_length=250)
    prescription = models.TextField(blank=True, null=True)
    dosage = models.TextField(blank=True, null=True)
    debut = models.DateTimeField(default=timezone.now)  # Champ pour l'heure de début de la consultation
    fin = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nom_patient} {self.prenom_patient}"

class ExamenDetail(models.Model):
    nom = models.CharField(max_length=30)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.nom}"
    

class Examen(models.Model):
    patient = models.ForeignKey(Vision, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    nom_examen = models.ForeignKey(ExamenDetail, on_delete=models.CASCADE)
    resultat = models.FileField(upload_to='resultats/', blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - Examen: {self.nom}"

class Laser(models.Model):
    patient = models.ForeignKey(SalleDAttente, on_delete=models.CASCADE)
    medecin = models.ForeignKey(MedecinOphalmo, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    information = models.CharField(max_length=250)

    def __str__(self):
        return f"Laser pour {self.patient} {self.Medecin}"


class TypePiqure(models.Model):
    nom = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.nom


class Piqure(models.Model):
    patient = models.ForeignKey(SalleDAttente, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    type = models.ForeignKey(TypePiqure, on_delete=models.CASCADE)
    detail = models.TextField()

    def __str__(self):
        return f"Piqure pour {self.patient}- Type: {self.type_piqure}"



class TypeOperation(models.Model):
    nom = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nom


class Operation(models.Model):
    patient = models.ForeignKey(SalleDAttente, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeOperation, on_delete=models.CASCADE)
    medecin = models.ForeignKey(MedecinOphalmo, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    detail = models.TextField()

    def __str__(self):
        return f"Opération pour {self.patient}- Type: {self.type_operation}"

class Rendez_vous_en_ligne(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    adresse = models.CharField(max_length=70)
    telephone = models.CharField(max_length=15)
    objet = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.objet} {self.nom}"


class Rendez_vous_local(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    OBJET_CHOICES = (
        ('laser', 'Laser'),
        ('consultation', 'Consultation'),
        ('examen', 'Examen'),
        ('operation', 'Operation'),
        ('lunette', 'Lunette'),
        ('piqure', 'Piqure'),
    )
    objet = models.CharField(max_length=25,choices=OBJET_CHOICES )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.objet} {self.nom}"



from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Caissiere(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


from django.db import models

class PiqureDetail(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nom


class LaserDetail(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f" {self.nom}"

class OperationDetail(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f" {self.nom}"

class ConsultationDetail(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f" {self.nom}"

# Ajoutez d'autres modèles de détail pour d'autres types d'examen si nécessaire
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from django.db import models
from django.utils import timezone

# Modèle pour gérer les types de paiement
class ModePaiement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

from django.db import models
from django.utils import timezone

# Modèle pour gérer les types de paiement
class ModePaiement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle pour gérer les dettes des patients
class DettePatient(models.Model):
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Dette de {self.nom_patient} {self.prenom_patient}"

# Modèle de facture pour les examens
class FactureExamen(models.Model):
    factureexamen_id = models.AutoField(primary_key=True)
    caissiere = models.ForeignKey(Caissiere, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    examen = models.ForeignKey(ExamenDetail, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    special = models.BooleanField(default=False)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f" {self.examen}"


# Modèle de facture pour les lasers
class FactureLaser(models.Model):
    facturelaser_id = models.AutoField(primary_key=True)
    caissiere = models.ForeignKey(Caissiere, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    laser = models.ForeignKey(LaserDetail, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    special = models.BooleanField(default=False)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f" {self.laser}"

# Modèle de facture pour les opérations
class FactureOperation(models.Model):
    factureoperation_id = models.AutoField(primary_key=True)
    caissiere = models.ForeignKey(Caissiere, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    operation = models.ForeignKey(OperationDetail, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    special = models.BooleanField(default=False)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f" {self.operation}"

# Modèle de facture pour les piqûres
class FacturePiqure(models.Model):
    facturepiqure_id = models.AutoField(primary_key=True)
    caissiere = models.ForeignKey(Caissiere, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    piqure = models.ForeignKey(PiqureDetail, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    special = models.BooleanField(default=False)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f" {self.piqure}"

# Modèle de facture pour les consultations
class FactureConsultation(models.Model):
    factureconsultation_id = models.AutoField(primary_key=True)
    caissiere = models.ForeignKey(Caissiere, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    nom_patient = models.CharField(max_length=100)
    prenom_patient = models.CharField(max_length=100)
    Consultation = models.ForeignKey(ConsultationDetail, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    special = models.BooleanField(default=False)
    mode_paiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f" {self.Consultation}"
