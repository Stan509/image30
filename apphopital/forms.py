from django import forms
from .models import *
from django.core import validators
from django.forms import DateTimeInput

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'sexe', 'numero_dossier', 'date_de_naissance', 'profession', 'adresse', 'telephone', 'assurance', 'date']
        
class SalleDAttenteForm(forms.ModelForm):
    heure_arrivee = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False  # Permet la saisie manuelle
    )

    class Meta:
        model = SalleDAttente
        fields = ['nom', 'prenom', 'numero_dossier', 'heure_arrivee', 'traitement']


class VisionForm(forms.ModelForm):
    class Meta:
        model = Vision
        fields = ['id', 'patient', 'date', 'cylindre_os', 'cylindre_od', 'sphere_od', 'sphere_os', 'axe_od', 'axe_os', 'tension_od', 'tension_os', 'vision_os', 'vision_od']

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['id', 'patient', 'date', 'nom_examen', 'resultat']


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['id', 'patient', 'date', 'medecin', 'debut', 'motif_consultation', 'avis', 'prescription', 'dosage', 'fin']


class LaserForm(forms.ModelForm):
    class Meta:
        model = Laser
        fields = ['id', 'patient','medecin', 'date', 'information']


class PiqureForm(forms.ModelForm):
    class Meta:
        model = Piqure
        fields = ['id', 'patient', 'date', 'type', 'detail']


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['id', 'patient', 'type', 'medecin', 'date',  'detail']




class Rendez_vous_localForm(forms.ModelForm):
    # Votre définition de formulaire ici

    class Meta:
        model = Rendez_vous_local
        fields = ['id', 'nom', 'prenom', 'telephone', 'objet', 'date']


class Rendez_vous_en_ligneForm(forms.ModelForm):
    class Meta:
        model = Rendez_vous_en_ligne
        fields = ['id', 'nom', 'prenom', 'adresse', 'telephone', 'objet', 'date']


# Formulaire pour le modèle DettePatient
class DettePatientForm(forms.ModelForm):
    class Meta:
        model = DettePatient
        fields = '__all__'

# Formulaire pour le modèle FactureExamen
class FactureExamenForm(forms.ModelForm):
    class Meta:
        model = FactureExamen
        fields = '__all__'

# Formulaire pour le modèle FactureLaser
class FactureLaserForm(forms.ModelForm):
    class Meta:
        model = FactureLaser
        fields = '__all__'

# Formulaire pour le modèle FactureOperation
class FactureOperationForm(forms.ModelForm):
    class Meta:
        model = FactureOperation
        fields = '__all__'

# Formulaire pour le modèle FacturePiqure
class FacturePiqureForm(forms.ModelForm):
    class Meta:
        model = FacturePiqure
        fields = '__all__'

# Formulaire pour le modèle FactureConsultation
class FactureConsultationForm(forms.ModelForm):
    class Meta:
        model = FactureConsultation
        fields = '__all__'