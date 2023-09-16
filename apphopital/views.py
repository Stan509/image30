from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import Rendez_vous_localForm
from .models import Rendez_vous_local
from datetime import date
from django.contrib.auth.decorators import login_required
from apphopital.admin import VisionAdmin
from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
 # Importez le modèle Vision
from django.db.models import IntegerField
from django.shortcuts import render, HttpResponseRedirect
from .forms import PatientForm
from .models import Patient, ExamenDetail, Examen
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q 


def acceuil(request):
    return render(request, 'acceuil.html') 

def assistant_view(request):
    return render(request, 'assistant.html')

def equipe_view(request):
    return render(request, 'equipe.html')

def a_propos_view(request):
    return render(request, 'apropos.html')

def attente_view(request):
    return render(request, 'attente.html')


def consultation_view(request):
    return render(request, 'consultation.html')

def rendez_vous_en_ligne_view(request):
    return render(request, 'rdvligne.html')




def examen_view(request):
    return render(request, 'examen.html')

def piqure_view(request):
    return render(request, 'piqure.html')


def operation_view(request):
    return render(request, 'operation.html')

def laser_view(request):
    return render(request, 'laser.html')



def vision_view(request):
    return render(request, 'vision.html')

def rendez_vous_local_view(request):
    return render(request, 'rendez_vous_local.html')


@login_required
def patient_view(request):
    patients = Patient.objects.all()  # Récupérez tous les patients depuis la base de données
    search_term = request.GET.get('search')
    if search_term:
        patients = patients.filter(Q(nom__icontains=search_term) | Q(prenom__icontains=search_term))

    # Filtrer par sexe si une option est sélectionnée
    gender = request.GET.get('gender')
    if gender:
        patients = patients.filter(sexe=gender)

    # Filtrer par date de naissance si une date est spécifiée
    birthdate = request.GET.get('birthdate')
    if birthdate:
        patients = patients.filter(date_de_naissance=birthdate)

    # Pagination
    paginator = Paginator(patients, 10)  # Afficher 10 résultats par page
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    if request.method == 'POST':
        fm = PatientForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['nom']
            pm = fm.cleaned_data['prenom']
            sm = fm.cleaned_data['sexe']
            ndm = fm.cleaned_data['numero_dossier']
            ddnm = fm.cleaned_data['date_de_naissance']
            prm = fm.cleaned_data['profession']
            am = fm.cleaned_data['adresse']
            tm = fm.cleaned_data['telephone']
            asm = fm.cleaned_data['assurance']
            dm = fm.cleaned_data['date']
            reg = Patient(nom=nm, prenom=pm, sexe=sm, numero_dossier=ndm, date_de_naissance=ddnm, profession=prm, adresse=am, telephone=tm, assurance=asm, date=dm)
            reg.save()
            fm = PatientForm()
    else:
        fm = PatientForm()
    
    return render(request, 'patient.html', {'form': fm, 'patients': patients})





from django.contrib import messages
from django.shortcuts import render, redirect

def modifier_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)  # Récupérez le patient depuis la base de données

    if request.method == 'POST':
        fm = PatientForm(request.POST, instance=patient)  # Utilisez le même formulaire et pré-remplissez-le avec les données du patient
        if fm.is_valid():
            fm.save()  # Enregistrez les modifications dans la base de données

            # Ajoutez un message de succès
            messages.success(request, "Les informations du patient ont été modifiées avec succès.")
            
            # Redirigez l'utilisateur vers la page 'patient'
            return redirect('patient')

    else:
        fm = PatientForm(instance=patient)  # Utilisez le même formulaire pré-rempli avec les données du patient

    return render(request, 'modifier_patient.html', {'form': fm, 'patient': patient})




    
def LogoutView(request):
    return redirect("acceuil")

def connexion_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return render(request, 'patient.html')
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")
    form = AuthenticationForm()
    return render(request, "connexion.html", {"form": form})



from django.shortcuts import render, redirect
from .models import Patient

def delete_patient(request, patient_id):
    # Check if the user is authorized to delete the patient
    if request.user.has_perm('patients.delete_patient', patient):
        patient = Patient.objects.get(pk=patient_id)
        patient.delete()
        return redirect('patient')
    else:
        return render(request, 'patient.html')
    




from .models import SalleDAttente
from .forms import SalleDAttenteForm
from django.shortcuts import render
@login_required
def attente_view(request):
    patients_attente = SalleDAttente.objects.all()  # Récupérez tous les patients en attente depuis la base de données

    if request.method == 'POST':
        fm = SalleDAttenteForm(request.POST)
        if fm.is_valid():
            nom = fm.cleaned_data['nom']
            prenom = fm.cleaned_data['prenom']
            numero_dossier = fm.cleaned_data['numero_dossier']
            traitement = fm.cleaned_data['traitement']
            # Pas besoin de définir l'heure d'arrivée, car elle est automatiquement définie à l'heure actuelle

            # Créez un nouvel enregistrement en attente
            attente = SalleDAttente(nom=nom, prenom=prenom, numero_dossier=numero_dossier, traitement=traitement)
            attente.save()
            
            fm = SalleDAttenteForm()
    else:
        fm = SalleDAttenteForm()
        patients_attente = SalleDAttente.objects.all()
    return render(request, 'attente.html', {'form': fm, 'patients_attente': patients_attente})

# views.py
from django.shortcuts import get_object_or_404, redirect

def supprimer_patient_attente(request, patient_id):
    patient = get_object_or_404(SalleDAttente, id=patient_id)
    
    if request.method == 'POST':
        # Supprimez le patient en attente
        patient.delete()
        return redirect('attente_view')  # Redirigez vers la liste des patients en attente
    
    return render(request, 'confirmation_suppression.html', {'patient': patient})



from .models import Vision
from .forms import VisionForm
from django.shortcuts import render
@login_required
def vision_view(request):
    visions = Vision.objects.all()  # Récupérez toutes les données de vision depuis la base de données

    if request.method == 'POST':
        fm = VisionForm(request.POST)
        if fm.is_valid():
            patient = fm.cleaned_data['patient']
            date = fm.cleaned_data['date']
            cylindre_os = fm.cleaned_data['cylindre_os']
            cylindre_od = fm.cleaned_data['cylindre_od']
            sphere_od = fm.cleaned_data['sphere_od']
            sphere_os = fm.cleaned_data['sphere_os']
            axe_od = fm.cleaned_data['axe_od']
            axe_os = fm.cleaned_data['axe_os']
            tension_od = fm.cleaned_data['tension_od']
            tension_os = fm.cleaned_data['tension_os']
            vision_os = fm.cleaned_data['vision_os']
            vision_od = fm.cleaned_data['vision_od']

            # Créez un nouvel enregistrement de vision
            vision = Vision(
                patient=patient,
                date=date,
                cylindre_os=cylindre_os,
                cylindre_od=cylindre_od,
                sphere_od=sphere_od,
                sphere_os=sphere_os,
                axe_od=axe_od,
                axe_os=axe_os,
                tension_od=tension_od,
                tension_os=tension_os,
                vision_os=vision_os,
                vision_od=vision_od
            )
            vision.save()

            fm = VisionForm()
    else:
        fm = VisionForm()
        visions = Vision.objects.all()  # Correction ici

    return render(request, 'vision.html', {'form': fm, 'visions': visions})



from .models import Consultation
from .forms import ConsultationForm
from django.shortcuts import render
@login_required
def consultation_view(request):
    consultations = Consultation.objects.all()  # Récupérez toutes les données de consultation depuis la base de données

    if request.method == 'POST':
        fm = ConsultationForm(request.POST)
        if fm.is_valid():
            patient = fm.cleaned_data['patient']
            date = fm.cleaned_data['date']
            medecin = fm.cleaned_data['medecin']
            debut = fm.cleaned_data['debut']
            motif_consultation = fm.cleaned_data['motif_consultation']
            avis = fm.cleaned_data['avis']
            prescription = fm.cleaned_data['prescription']
            dosage = fm.cleaned_data['dosage']

            # Créez un nouvel enregistrement de consultation
            consultation = Consultation(
                patient=patient,
                date=date,
                medecin=medecin,
                debut=debut,
                motif_consultation=motif_consultation,
                avis=avis,
                prescription=prescription,
                dosage=dosage
            )
            consultation.save()

            fm = ConsultationForm()
    else:
        fm = ConsultationForm()

    return render(request, 'consultation.html', {'form': fm, 'consultations': consultations})


from .models import Examen
from .forms import ExamenForm
from django.shortcuts import render
@login_required
def examen_view(request):
    examens = Examen.objects.all()  # Récupérez toutes les données d'examen depuis la base de données

    if request.method == 'POST':
        fm = ExamenForm(request.POST, request.FILES)
        if fm.is_valid():
            patient = fm.cleaned_data['patient']
            date = fm.cleaned_data['date']
            nom_examen = fm.cleaned_data['nom_examen']
            resultat = fm.cleaned_data['resultat']

            # Créez un nouvel enregistrement d'examen
            examen = Examen(
                patient=patient,
                date=date,
                nom_examen=nom_examen,
                resultat=resultat
            )
            examen.save()

            fm = ExamenForm()
    else:
        fm = ExamenForm()
    examens = Examen.objects.all()
    return render(request, 'examen.html', {'form': fm, 'examens': examens})


from .models import Laser
from .forms import LaserForm
from django.shortcuts import render
@login_required
def laser_view(request):
    lasers = Laser.objects.all()  # Récupérez toutes les données Laser depuis la base de données

    if request.method == 'POST':
        fm = LaserForm(request.POST)
        if fm.is_valid():
            patient = fm.cleaned_data['patient']
            medecin = fm.cleaned_data['medecin']
            date = fm.cleaned_data['date']
            information = fm.cleaned_data['information']

            # Créez un nouvel enregistrement Laser
            laser = Laser(
                patient=patient,
                medecin=medecin,
                date=date,
                information=information
            )
            laser.save()

            fm = LaserForm()
    else:
        fm = LaserForm()

    return render(request, 'laser.html', {'form': fm, 'lasers': lasers})


from .models import Piqure
from .forms import PiqureForm
from django.shortcuts import render
@login_required
def piqure_view(request):
    piqures = Piqure.objects.all()  # Récupérez toutes les données Piqure depuis la base de données

    if request.method == 'POST':
        fm = PiqureForm(request.POST)
        if fm.is_valid():
            patient = fm.cleaned_data['patient']
            date = fm.cleaned_data['date']
            type_piqure = fm.cleaned_data['type']
            detail = fm.cleaned_data['detail']

            # Créez un nouvel enregistrement Piqure
            piqure = Piqure(
                patient=patient,
                date=date,
                type=type_piqure,
                detail=detail
            )
            piqure.save()

            fm = PiqureForm()
    else:
        fm = PiqureForm()

    return render(request, 'piqure.html', {'form': fm, 'piqures': piqures})



from .models import Operation
from .forms import OperationForm
from django.shortcuts import render
@login_required
def operation_view(request):
    operations = Operation.objects.all()  # Récupérez toutes les données Operation depuis la base de données

    if request.method == 'POST':
        fm = OperationForm(request.POST)
        if fm.is_valid():
            patient = fm.cleaned_data['patient']
            type_operation = fm.cleaned_data['type']
            medecin = fm.cleaned_data['medecin']
            date = fm.cleaned_data['date']
            detail = fm.cleaned_data['detail']

            # Créez un nouvel enregistrement Operation
            operation = Operation(
                patient=patient,
                type=type_operation,
                medecin=medecin,
                date=date,
                detail=detail
            )
            operation.save()

            fm = OperationForm()
    else:
        fm = OperationForm()

    return render(request, 'operation.html', {'form': fm, 'operations': operations})


from .models import Rendez_vous_en_ligne
from .forms import Rendez_vous_en_ligneForm
from django.shortcuts import render
@login_required
def rendez_vous_en_ligne_view(request):
    rendez_vous = Rendez_vous_en_ligne.objects.all()  # Récupérez tous les rendez-vous en ligne depuis la base de données

    if request.method == 'POST':
        fm = Rendez_vous_en_ligneForm(request.POST)
        if fm.is_valid():
            nom = fm.cleaned_data['nom']
            prenom = fm.cleaned_data['prenom']
            adresse = fm.cleaned_data['adresse']
            telephone = fm.cleaned_data['telephone']
            objet = fm.cleaned_data['objet']
            date = fm.cleaned_data['date']

            # Créez un nouvel enregistrement Rendez_vous_en_ligne
            rendez_vous = Rendez_vous_en_ligne(
                nom=nom,
                prenom=prenom,
                adresse=adresse,
                telephone=telephone,
                objet=objet,
                date=date
            )
            rendez_vous.save()

            fm = Rendez_vous_en_ligneForm()
    else:
        fm = Rendez_vous_en_ligneForm()

    return render(request, 'rendez_vous_en_ligne.html', {'form': fm, 'rendez_vous': rendez_vous})


from .models import Rendez_vous_local
from .forms import Rendez_vous_localForm
from django.shortcuts import render
@login_required
def rendez_vous_local_view(request):
    rendez_vous = Rendez_vous_local.objects.all()  # Récupérez tous les rendez-vous locaux depuis la base de données

    if request.method == 'POST':
        fm = Rendez_vous_localForm(request.POST)
        if fm.is_valid():
            nom = fm.cleaned_data['nom']
            prenom = fm.cleaned_data['prenom']
            telephone = fm.cleaned_data['telephone']
            objet = fm.cleaned_data['objet']
            date = fm.cleaned_data['date']

            # Créez un nouvel enregistrement Rendez_vous_local
            nouveau_rendez_vous = Rendez_vous_local(
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                objet=objet,
                date=date
            )
            nouveau_rendez_vous.save()

            fm = Rendez_vous_localForm()
    else:
        fm = Rendez_vous_localForm()

    return render(request, 'rendez_vous_local.html', {'form': fm, 'rendez_vous': rendez_vous})


    # Filtrer les rendez-vous pour obtenir uniquement ceux du jour actuel



from django.shortcuts import render, get_object_or_404, redirect
from .models import FactureExamen
from .forms import FactureExamenForm

from django.shortcuts import render, redirect
from .forms import FactureExamenForm
@login_required
def ajouter_facture_examen(request):
    if request.method == 'POST':
        form = FactureExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_view')  # Redirection vers la page facture.html après l'ajout
    else:
        form = FactureExamenForm()

    return redirect('facture_view')
@login_required

def facture_view(request):
    return render(request, 'facture.html')

@login_required
def facture_examen_view(request):
    factures_examen = FactureExamen.objects.all()

    if request.method == 'POST':
        form = FactureExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_examen_view')
    else:
        form = FactureExamenForm()

    context = {'factures_examen': factures_examen, 'form': form}
    return render(request, 'factureexamen.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .forms import FactureConsultationForm  # Assurez-vous d'importer le bon formulaire
from .models import FactureConsultation  # Assurez-vous d'importer le bon modèle
@login_required
def ajouter_facture_consultation(request):
    if request.method == 'POST':
        form = FactureConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_view')  # Redirection vers la page facture.html après l'ajout
    else:
        form = FactureConsultationForm()

    return redirect('facture_view')
@login_required
def facture_consultation_view(request):
    factures_consultation = FactureConsultation.objects.all()

    if request.method == 'POST':
        form = FactureConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_consultation_view')
    else:
        form = FactureConsultationForm()

    context = {'factures_consultation': factures_consultation, 'form': form}
    return render(request, 'factureconsultation.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .forms import FactureLaserForm  # Assurez-vous d'importer le bon formulaire
from .models import FactureLaser  # Assurez-vous d'importer le bon modèle
@login_required
def ajouter_facture_laser(request):
    if request.method == 'POST':
        form = FactureLaserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_view')  # Redirection vers la page facture.html après l'ajout
    else:
        form = FactureLaserForm()

    return redirect('facture_view')

@login_required
def facture_laser_view(request):
    factures_laser = FactureLaser.objects.all()

    if request.method == 'POST':
        form = FactureLaserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_laser_view')
    else:
        form = FactureLaserForm()

    context = {'factures_laser': factures_laser, 'form': form}
    return render(request, 'facturelaser.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .forms import FacturePiqureForm  # Assurez-vous d'importer le bon formulaire
from .models import FacturePiqure  # Assurez-vous d'importer le bon modèle


@login_required
def ajouter_facture_piqure(request):
    if request.method == 'POST':
        form = FacturePiqureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_view')  # Redirection vers la page facture.html après l'ajout
    else:
        form = FacturePiqureForm()

    return redirect('facture_view')


from django.shortcuts import render, redirect, get_object_or_404
from .forms import FactureOperationForm  # Assurez-vous d'importer le bon formulaire
from .models import FactureOperation  # Assurez-vous d'importer le bon modèle


@login_required
def ajouter_facture_operation(request):
    if request.method == 'POST':
        form = FactureOperationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_view')  # Redirection vers la page facture.html après l'ajout
    else:
        form = FactureOperationForm()

    return redirect('facture_view')


@login_required
def facture_operation_view(request):
    factures_operation = FactureOperation.objects.all()

    if request.method == 'POST':
        form = FactureOperationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_operation_view')
    else:
        form = FactureOperationForm()

    context = {'factures_operation': factures_operation, 'form': form}
    return render(request, 'factureoperation.html', context)


# views.py
from django.shortcuts import render, redirect
from .models import FacturePiqure
from .forms import FacturePiqureForm


@login_required
def facture_piqure_view(request):
    factures_piqure = FacturePiqure.objects.all()
    form = FacturePiqureForm()  # Instancier le formulaire vide

    if request.method == 'POST':
        form = FacturePiqureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facture_piqure_view')

    context = {'factures_piqure': factures_piqure, 'form': form}
    return render(request, 'facture.html', context)


from django.shortcuts import render, redirect
from .models import FactureExamen  # Assurez-vous d'importer correctement votre modèle FactureExamen



@login_required
def facture_examen_view(request):
    factures_examen = FactureExamen.objects.all()  # Récupérez toutes les factures d'examen depuis la base de données

    if request.method == 'POST':
        form = FactureExamenForm(request.POST)
        if form.is_valid():
            # Obtenez les données du formulaire validé
            caissiere = form.cleaned_data['caissiere']
            date = form.cleaned_data['date']
            nom_patient = form.cleaned_data['nom_patient']
            prenom_patient = form.cleaned_data['prenom_patient']
            examen = form.cleaned_data['examen']
            quantite = form.cleaned_data['quantite']
            montant_paye = form.cleaned_data['montant_paye']
            total = form.cleaned_data['total']
            special = form.cleaned_data['special']
            mode_paiement = form.cleaned_data['mode_paiement']
            prix = form.cleaned_data['prix']

            # Créez un nouvel enregistrement de facture d'examen
            facture_examen = FactureExamen(
                caissiere=caissiere,
                date=date,
                nom_patient=nom_patient,
                prenom_patient=prenom_patient,
                examen=examen,
                quantite=quantite,
                montant_paye=montant_paye,
                total=total,
                special=special,
                mode_paiement=mode_paiement,
                prix=prix
            )
            facture_examen.save()

            form = FactureExamenForm()  # Réinitialisez le formulaire après l'ajout de la facture d'examen
    else:
        form = FactureExamenForm()
        factures_examen = FactureExamen.objects.all()

    return render(request, 'factureexamen.html', {'form': form, 'factures_examen': factures_examen})


def facex_view(request):
    factures_examen = FactureExamen.objects.all()
    return render(request, 'facture.html', {'factures_examen': factures_examen})


from django.shortcuts import render, redirect  # Ajoutez redirect pour la redirection
from .models import FactureLaser
from .forms import FactureLaserForm  # Assurez-vous d'importer le formulaire FactureLaserForm




@login_required
def facture_laser_view(request):
    factures_laser = FactureLaser.objects.all()  # Récupérez toutes les factures laser depuis la base de données

    if request.method == 'POST':
        form = FactureLaserForm(request.POST)
        if form.is_valid():
            # Obtenez les données du formulaire validé
            caissiere = form.cleaned_data['caissiere']
            date = form.cleaned_data['date']
            nom_patient = form.cleaned_data['nom_patient']
            prenom_patient = form.cleaned_data['prenom_patient']
            laser = form.cleaned_data['laser']
            quantite = form.cleaned_data['quantite']
            montant_paye = form.cleaned_data['montant_paye']
            total = form.cleaned_data['total']
            special = form.cleaned_data['special']
            mode_paiement = form.cleaned_data['mode_paiement']
            prix = form.cleaned_data['prix']

            # Créez un nouvel enregistrement de facture laser
            facture_laser = FactureLaser(
                caissiere=caissiere,
                date=date,
                nom_patient=nom_patient,
                prenom_patient=prenom_patient,
                laser=laser,
                quantite=quantite,
                montant_paye=montant_paye,
                total=total,
                special=special,
                mode_paiement=mode_paiement,
                prix=prix
            )
            facture_laser.save()

            form = FactureLaserForm()  # Réinitialisez le formulaire après l'ajout de la facture laser

    else:
        form = FactureLaserForm()
        factures_laser = FactureLaser.objects.all()

    return render(request, 'facturelaser.html', {'form': form, 'factures_laser': factures_laser})



@login_required
def facture_view(request):
    factures_laser = FactureLaser.objects.all()
    return render(request, 'facture.html', {'factures_laser': factures_laser})

from django.shortcuts import render
from .models import FactureExamen

def facex_view(request):
    factures_examen = FactureExamen.objects.all()
    return render(request, 'facture.html', {'factures_examen': factures_examen})



from django.shortcuts import render
from .models import FactureExamen, FactureConsultation, FacturePiqure, FactureOperation, FactureLaser



@login_required
def facture_view(request):
    factures_examen = FactureExamen.objects.all()
    factures_consultation = FactureConsultation.objects.all()
    factures_piqure = FacturePiqure.objects.all()
    factures_operation = FactureOperation.objects.all()
    factures_laser = FactureLaser.objects.all()

    return render(request, 'facture.html', {
        'factures_examen': factures_examen,
        'factures_consultation': factures_consultation,
        'factures_piqure': factures_piqure,
        'factures_operation': factures_operation,
        'factures_laser': factures_laser,
    })





@login_required
def facture_consultation_view(request):
    factures_consultation = FactureConsultation.objects.all()

    if request.method == 'POST':
        form = FactureConsultationForm(request.POST)
        if form.is_valid():
            # Obtenir les données du formulaire validé
            caissiere = form.cleaned_data['caissiere']
            date = form.cleaned_data['date']
            nom_patient = form.cleaned_data['nom_patient']
            prenom_patient = form.cleaned_data['prenom_patient']
            Consultation = form.cleaned_data['Consultation']
            quantite = form.cleaned_data['quantite']
            montant_paye = form.cleaned_data['montant_paye']
            total = form.cleaned_data['total']
            special = form.cleaned_data['special']
            mode_paiement = form.cleaned_data['mode_paiement']
            prix = form.cleaned_data['prix']

            # Créer un nouvel enregistrement de facture de consultation
            facture_consultation = FactureConsultation(
                caissiere=caissiere,
                date=date,
                nom_patient=nom_patient,
                prenom_patient=prenom_patient,
                Consultation=Consultation,
                quantite=quantite,
                montant_paye=montant_paye,
                total=total,
                special=special,
                mode_paiement=mode_paiement,
                prix=prix
            )
            facture_consultation.save()

            form = FactureConsultationForm()  # Réinitialiser le formulaire après l'ajout de la facture de consultation
    else:
        form = FactureConsultationForm()
        factures_consultation = FactureConsultation.objects.all()

    return render(request, 'factureconsultation.html', {'form': form, 'factures_consultation': factures_consultation})



@login_required
def facture_piqure_view(request):
    factures_piqure = FacturePiqure.objects.all()

    if request.method == 'POST':
        form = FacturePiqureForm(request.POST)
        if form.is_valid():
            # Obtenir les données du formulaire validé
            caissiere = form.cleaned_data['caissiere']
            date = form.cleaned_data['date']
            nom_patient = form.cleaned_data['nom_patient']
            prenom_patient = form.cleaned_data['prenom_patient']
            piqure = form.cleaned_data['piqure']
            quantite = form.cleaned_data['quantite']
            montant_paye = form.cleaned_data['montant_paye']
            total = form.cleaned_data['total']
            special = form.cleaned_data['special']
            mode_paiement = form.cleaned_data['mode_paiement']
            prix = form.cleaned_data['prix']

            # Créer un nouvel enregistrement de facture de piqure
            facture_piqure = FacturePiqure(
                caissiere=caissiere,
                date=date,
                nom_patient=nom_patient,
                prenom_patient=prenom_patient,
                piqure=piqure,
                quantite=quantite,
                montant_paye=montant_paye,
                total=total,
                special=special,
                mode_paiement=mode_paiement,
                prix=prix
            )
            facture_piqure.save()

            form = FacturePiqureForm()  # Réinitialiser le formulaire après l'ajout de la facture de piqure
    else:
        form = FacturePiqureForm()
        factures_piqure = FacturePiqure.objects.all()

    return render(request, 'facturepiqure.html', {'form': form, 'factures_piqure': factures_piqure})




@login_required
def facture_operation_view(request):
    factures_operation = FactureOperation.objects.all()

    if request.method == 'POST':
        form = FactureOperationForm(request.POST)
        if form.is_valid():
            # Obtenir les données du formulaire validé
            caissiere = form.cleaned_data['caissiere']
            date = form.cleaned_data['date']
            nom_patient = form.cleaned_data['nom_patient']
            prenom_patient = form.cleaned_data['prenom_patient']
            operation = form.cleaned_data['operation']
            quantite = form.cleaned_data['quantite']
            montant_paye = form.cleaned_data['montant_paye']
            total = form.cleaned_data['total']
            special = form.cleaned_data['special']
            mode_paiement = form.cleaned_data['mode_paiement']
            prix = form.cleaned_data['prix']

            # Créer un nouvel enregistrement de facture d'opération
            facture_operation = FactureOperation(
                caissiere=caissiere,
                date=date,
                nom_patient=nom_patient,
                prenom_patient=prenom_patient,
                operation=operation,
                quantite=quantite,
                montant_paye=montant_paye,
                total=total,
                special=special,
                mode_paiement=mode_paiement,
                prix=prix
            )
            facture_operation.save()

            form = FactureOperationForm()  # Réinitialiser le formulaire après l'ajout de la facture d'opération
    else:
        form = FactureOperationForm()
        factures_operation = FactureOperation.objects.all()

    return render(request, 'factureoperation.html', {'form': form, 'factures_operation': factures_operation})
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generer_pdf(request, factureexamen_id):
    # Obtenez la facture d'examen à partir du nom du patient
    factureexamen = get_object_or_404(FactureExamen, nom_patient=factureexamen_id)

    # Générez le contenu HTML à partir d'un modèle
    template_path = 'impression.html'  # Remplacez par le chemin de votre modèle PDF
    context = {'factureexamen': factureexamen}
    template = get_template(template_path)
    html = template.render(context)

    # Créez un objet HttpResponse avec l'en-tête PDF approprié
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_examen_{factureexamen.nom_patient}.pdf"'

    # Créez le PDF à partir du contenu HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # S'il y a une erreur lors de la création du PDF, retournez une réponse vide avec un code d'erreur approprié
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF.', status=500)

    return response


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generer_pdf_piqure(request, facturepiqure_id):
    # Obtenez la facture de piqûre à partir de l'identifiant
    facturepiqure = get_object_or_404(FacturePiqure, nom_patient=facturepiqure_id)

    # Générez le contenu HTML à partir d'un modèle
    template_path = 'impressionpiqure.html'  # Remplacez par le chemin de votre modèle PDF pour la piqûre
    context = {'facturepiqure': facturepiqure}
    template = get_template(template_path)
    html = template.render(context)

    # Créez un objet HttpResponse avec l'en-tête PDF approprié
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_piqure_{facturepiqure.nom_patient}.pdf"'

    # Créez le PDF à partir du contenu HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # S'il y a une erreur lors de la création du PDF, retournez une réponse vide avec un code d'erreur approprié
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF de piqûre.', status=500)

    return response

def generer_pdf_operation(request, factureoperation_id):
    # Obtenez la facture d'opération à partir de l'identifiant
    factureoperation = get_object_or_404(FactureOperation, nom_patient=factureoperation_id)

    # Générez le contenu HTML à partir d'un modèle
    template_path = 'impressionoperation.html'  # Remplacez par le chemin de votre modèle PDF pour l'opération
    context = {'factureoperation': factureoperation}
    template = get_template(template_path)
    html = template.render(context)

    # Créez un objet HttpResponse avec l'en-tête PDF approprié
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_operation_{factureoperation.nom_patient}.pdf"'

    # Créez le PDF à partir du contenu HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # S'il y a une erreur lors de la création du PDF, retournez une réponse vide avec un code d'erreur approprié
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF d\'opération.', status=500)

    return response

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generer_pdf_consultation(request, factureconsultation_id):
    # Obtenez la facture de consultation à partir de l'identifiant
    factureconsultation = get_object_or_404(FactureConsultation, nom_patient=factureconsultation_id)

    # Générez le contenu HTML à partir d'un modèle
    template_path = 'impressionconsul.html'  # Remplacez par le chemin de votre modèle PDF pour la consultation
    context = {'factureconsultation': factureconsultation}
    template = get_template(template_path)
    html = template.render(context)

    # Créez un objet HttpResponse avec l'en-tête PDF approprié
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_consultation_{factureconsultation.nom_patient}.pdf"'

    # Créez le PDF à partir du contenu HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # S'il y a une erreur lors de la création du PDF, retournez une réponse vide avec un code d'erreur approprié
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF de consultation.', status=500)

    return response

def generer_pdf_laser(request, facturelaser_id):
    # Obtenez la facture de laser à partir de l'identifiant
    facturelaser = get_object_or_404(FactureLaser, nom_patient=facturelaser_id)

    # Générez le contenu HTML à partir d'un modèle
    template_path = 'impressionlaser.html'  # Remplacez par le chemin de votre modèle PDF pour le laser
    context = {'facturelaser': facturelaser}
    template = get_template(template_path)
    html = template.render(context)

    # Créez un objet HttpResponse avec l'en-tête PDF approprié
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_laser_{facturelaser.nom_patient}.pdf"'

    # Créez le PDF à partir du contenu HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # S'il y a une erreur lors de la création du PDF, retournez une réponse vide avec un code d'erreur approprié
    if pisa_status.err:
        return HttpResponse('Une erreur est survenue lors de la génération du PDF de laser.', status=500)

    return response

# Ajoutez des fonctions similaires pour les factures de piqûre et d'opération


from django.shortcuts import render





from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import os

def lecteur_view(request):
    # Récupérez l'URL du média depuis les paramètres GET
    media_url = request.GET.get('media_url', '')

    # Déterminez le type de média en fonction de l'URL
    if media_url.endswith('.pdf'):
        media_type = 'pdf'
    elif media_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        media_type = 'image'
    elif media_url.endswith(('.mp4', '.avi', '.mkv')):
        media_type = 'video'
    else:
        media_type = 'autre'

    # Renvoyez le média en fonction de son type
    if media_type == 'pdf':
        # Si c'est un PDF, servez-le en tant que fichier téléchargeable
        media_path = os.path.join(settings.MEDIA_ROOT, media_url)
        with open(media_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(media_path)}"'
            return response
    elif media_type in ('image', 'video'):
        # Si c'est une image ou une vidéo, renvoyez-la directement dans la page
        return render(request, 'lecteur.html', {'media_url': media_url, 'media_type': media_type})
    else:
        # Gérez d'autres types de médias ici si nécessaire
        return HttpResponse("Type de média non pris en charge.")


import os
from django.http import FileResponse

def lecteur_view(request):
    media_url = request.GET.get('media_url')
    
    # Construire le chemin absolu du fichier PDF
    file_path = os.path.join(settings.MEDIA_ROOT, media_url.lstrip('/'))
    
    if os.path.exists(file_path):
        # Si le fichier existe, renvoyez-le en tant que réponse de fichier
        with open(file_path, 'rb') as pdf_file:
            response = FileResponse(pdf_file)
            return response
    else:
        # Si le fichier n'existe pas, renvoyez une réponse d'erreur appropriée
        return HttpResponse('Le fichier demandé n\'existe pas.', status=404)


