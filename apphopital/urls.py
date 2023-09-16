
from django.urls import path, include
from .import views
from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('', acceuil, name='acceuil'),
    path('vision/', views.vision_view, name='vision_view'),
    path('patient/', views.patient_view, name='patient_view'),
    path('patient/', views.patient_view, name='patient'),
    path('modifier_patient/<int:patient_id>/', views.modifier_patient, name='modifier_patient'),
    path('delete/<int:id>/', delete_patient, name='supprimerpatient'),
    path('rendez_vous_local/', views.rendez_vous_local_view, name='rendez_vous_local_view'),
    path('rendez_vous_en_ligne/', views.rendez_vous_en_ligne_view, name='rendez_vous_en_ligne_view'),
    path('assistant/', views.assistant_view, name='assistant_view'),
    path('equipe/', views.equipe_view, name='equipe_view'),
    path('a_propos/', views.a_propos_view, name='a_propos_view'),
    path('attente/', views.attente_view, name='attente_view'),
    path('consultation/', views.consultation_view, name='consultation_view'),
    path('examen/', views.examen_view, name='examen_view'),
    path('facture/', views.facture_view, name='facture_view'),
    path('factureexamen/', views.facture_examen_view, name='facture_examen_view'),
    path('factureexamen/ajouter/', views.ajouter_facture_examen, name='ajouter_facture_examen'),
    path('factureconsultation/', views.facture_consultation_view, name='facture_consultation_view'),
    path('factureconsultation/ajouter/', views.ajouter_facture_consultation, name='ajouter_facture_consultation'),
    path('facturelaser/', views.facture_laser_view, name='facture_laser_view'),
    path('facturelaser/ajouter/', views.ajouter_facture_laser, name='ajouter_facture_laser'),
    path('facturepiqure/', views.facture_piqure_view, name='facture_piqure_view'),
    path('facturepiqure/ajouter/', views.ajouter_facture_piqure, name='ajouter_facture_piqure'),
    path('factureoperation/', views.facture_operation_view, name='facture_operation_view'),
    path('factureoperation/ajouter/', views.ajouter_facture_operation, name='ajouter_facture_operation'),
    path('laser/', views.laser_view, name='laser_view'),
    path('operation/', views.operation_view, name='operation_view'),
    path('piqure/', views.piqure_view, name='piqure_view'),
    path('attente/', views.attente_view, name='attente_view'),
    path('login/', views.connexion_view, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('factures_examen/', views.facex_view, name='factures_examen'),
    path('generer_pdf_piqure/<str:facturepiqure_id>/', views.generer_pdf_piqure, name='generer_pdf_piqure'),
    path('generer_pdf_piqure/<str:facturepiqure_id>/', views.generer_pdf_piqure, name='generer_pdf_piqure'),
    path('generer_pdf_operation/<str:factureoperation_id>/', views.generer_pdf_operation, name='generer_pdf_operation'),
    path('generer_pdf_consultation/<str:factureconsultation_id>/', views.generer_pdf_consultation, name='generer_pdf_consultation'),
    path('generer_pdf_laser/<str:facturelaser_id>/', views.generer_pdf_laser, name='generer_pdf_laser'),
    path('generer_pdf/<str:factureexamen_id>/', views.generer_pdf, name='generer_pdf'),
    path('lecteur/', views.lecteur_view, name='lecteur_view'),

    
    
]
