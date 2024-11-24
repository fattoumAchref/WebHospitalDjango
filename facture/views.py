# views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .forms import FactureForm
from .models import Facture
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Vérifie si l'utilisateur est un admin
def est_admin(user):
    return user.is_staff

@login_required
@user_passes_test(est_admin)
def ajouter_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_factures')  # Redirige vers une page listant toutes les factures
    else:
        form = FactureForm()
    return render(request, 'ajouter_facture.html', {'form': form})
@login_required
def facture_list(request):
    factures = Facture.objects.filter(patient=request.user)
    return render(request, 'factures_list.html', {'factures': factures})


def generate_pdf(request, facture_id):
    # Récupérer la facture à partir de la base de données
    try:
        facture = Facture.objects.get(id=facture_id)
    except Facture.DoesNotExist:
        return HttpResponse("Facture non trouvée", status=404)

    # Créer un objet HttpResponse avec le type MIME pour le PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'
    
    # Créer un objet canvas pour dessiner sur le PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # taille de la page PDF
    
    # Ajouter un titre au PDF
    pdf.setFont("Helvetica", 16)
    pdf.drawString(200, height - 40, "Facture")

    # Ajouter les données de la facture
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 80, f"Description : {facture.description}")
    pdf.drawString(50, height - 100, f"Montant : {facture.montant}")
    pdf.drawString(50, height - 120, f"Date d'émission : {facture.date_emission}")
    pdf.drawString(50, height - 140, f"Statut : {'Payée' if facture.est_payee else 'Non payée'}")
    pdf.drawString(50, height - 160, f"Date de paiement : {facture.date_paiement or 'Non renseignée'}")
    
    # Sauvegarder le PDF
    pdf.showPage()
    pdf.save()

    return response    # Exemple de données pour les factures
    factures = [
        {"description": "Consultation", "montant": 100, "date_emission": "2024-11-20", "est_payee": True, "date_paiement": "2024-11-22"},
        {"description": "Hospitalisation", "montant": 500, "date_emission": "2024-11-18", "est_payee": False, "date_paiement": None},
    ]
    
    # Créer un PDF pour chaque facture
    for i, facture in enumerate(factures):
        # Créer un objet HttpResponse avec le type MIME pour le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{i + 1}.pdf"'
        
        # Créer un objet canvas pour dessiner sur le PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        width, height = letter  # taille de la page PDF
        
        # Ajouter un titre au PDF
        pdf.setFont("Helvetica", 16)
        pdf.drawString(200, height - 40, "Facture")

        # Ajouter les données de la facture
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 80, f"Description : {facture['description']}")
        pdf.drawString(50, height - 100, f"Montant : {facture['montant']}")
        pdf.drawString(50, height - 120, f"Date d'émission : {facture['date_emission']}")
        pdf.drawString(50, height - 140, f"Statut : {'Payée' if facture['est_payee'] else 'Non payée'}")
        pdf.drawString(50, height - 160, f"Date de paiement : {facture['date_paiement'] or 'Non renseignée'}")
        
        # Sauvegarder le PDF
        pdf.showPage()
        pdf.save()

        # Retourner le PDF
        return response    # Récupère la facture en fonction de l'ID
    facture = get_object_or_404(Facture, id=facture_id)

    # Crée un contexte avec les données de la facture
    context = {
        'facture': facture,
    }

    # Rendu du template pour la facture, en utilisant render_to_string pour récupérer un string HTML
    html_string = render_to_string('facture_pdf_template.html', context)

    # Conversion du HTML en PDF avec WeasyPrint
    pdf_file = HTML(string=html_string).write_pdf()

    # Retourne le PDF dans la réponse HTTP
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{facture.id}.pdf"'

    return response