from django.contrib import admin
from .models import Patient, SalleDAttente, Vision, MedecinOphalmo, Consultation, ExamenDetail, Examen, Laser, TypePiqure, Piqure, TypeOperation, Operation, Rendez_vous_en_ligne, Rendez_vous_local, FactureExamen, FactureConsultation, FactureLaser, FactureOperation, FacturePiqure, LaserDetail, PiqureDetail, OperationDetail, ConsultationDetail, Caissiere, ModePaiement, DettePatient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'numero_dossier', 'date_de_naissance', 'profession', 'adresse', 'telephone', 'assurance', 'date')

@admin.register(SalleDAttente)
class SalleDAttenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'numero_dossier', 'heure_arrivee', 'traitement')

@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date', 'cylindre_os', 'cylindre_od', 'sphere_od', 'sphere_os', 'axe_od', 'axe_os', 'tension_od', 'tension_os', 'vision_os', 'vision_od')

@admin.register(MedecinOphalmo)
class MedcinOphtalmoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'specialite', 'numero_telephone')

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date', 'medecin', 'debut', 'motif_consultation', 'avis', 'prescription', 'dosage', 'fin')

@admin.register(ExamenDetail)
class ExamenDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix')

@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date', 'nom_examen', 'resultat')

@admin.register(Laser)
class LaserAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient','medecin', 'date', 'information')

@admin.register(TypePiqure)
class TypePiqureAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')


@admin.register(Piqure)
class PiqureAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date', 'type', 'detail')


@admin.register(TypeOperation)
class TypeOperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'type', 'medecin', 'date',  'detail',)


@admin.register(Rendez_vous_local)
class Rendez_vous_localAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'telephone', 'objet', 'date')


@admin.register(Rendez_vous_en_ligne)
class Rendez_vous_en_ligneAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'adresse', 'telephone', 'objet', 'date')

@admin.register(ModePaiement)
class ModePaiementAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')



@admin.register(DettePatient)
class DettePatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_patient', 'prenom_patient', 'telephone', 'montant', 'date')



@admin.register(FactureExamen)
class FactureExamenAdmin(admin.ModelAdmin):
    list_display = ('factureexamen_id', 'caissiere', 'date', 'nom_patient', 'prenom_patient', 'examen', 'quantite', 'montant_paye', 'total', 'special', 'mode_paiement', 'prix')



@admin.register(FactureLaser)
class FactureLaserAdmin(admin.ModelAdmin):
    list_display = ('facturelaser_id', 'caissiere', 'date', 'nom_patient', 'prenom_patient', 'laser', 'quantite', 'montant_paye', 'total', 'special', 'mode_paiement', 'prix')


@admin.register(FactureOperation)
class FactureOperationAdmin(admin.ModelAdmin):
    list_display = ('factureoperation_id', 'caissiere', 'date', 'nom_patient', 'prenom_patient', 'operation', 'quantite', 'montant_paye', 'total', 'special', 'mode_paiement', 'prix')


@admin.register(FacturePiqure)
class FacturePiqureAdmin(admin.ModelAdmin):
    list_display = ('facturepiqure_id', 'caissiere', 'date', 'nom_patient', 'prenom_patient', 'piqure', 'quantite', 'montant_paye', 'total', 'special', 'mode_paiement', 'prix')



@admin.register(FactureConsultation)
class FactureConsultationAdmin(admin.ModelAdmin):
    list_display = ('factureconsultation_id', 'caissiere', 'date', 'nom_patient', 'prenom_patient', 'Consultation', 'quantite', 'montant_paye', 'total', 'special', 'mode_paiement', 'prix')



@admin.register(OperationDetail)
class OperationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix')


@admin.register(LaserDetail)
class LaserDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix')

@admin.register(PiqureDetail)
class PiqureDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix')


@admin.register(ConsultationDetail)
class ConsultationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prix')

    @admin.register(Caissiere)
    class CassiereAdmin(admin.ModelAdmin):
        list_display = ('id', 'nom', 'prenom', 'numero_telephone')