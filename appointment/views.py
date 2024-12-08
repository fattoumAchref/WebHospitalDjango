from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from .forms import AppointmentForm

# Check if user is an administrator
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirect to a page listing appointments
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})

@login_required
def make_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Sauvegarder le rendez-vous
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Lier le rendez-vous à l'utilisateur connecté (patient)
            appointment.save()

            # Envoi de l'e-mail de confirmation
            subject = 'Confirmation de votre rendez-vous'
            message = f'Bonjour {request.user.first_name},\n\nVotre rendez-vous a été pris avec succès pour le {appointment.date}.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]  # L'email du patient qui a pris rendez-vous

            send_mail(subject, message, from_email, recipient_list)

            # Message de succès
            messages.success(request, "Votre rendez-vous a été pris avec succès.")
            return redirect('home')  # Ou redirigez où tu veux après succès
        else:
            messages.error(request, "Erreur lors de la prise de rendez-vous. Veuillez réessayer.")
    else:
        form = AppointmentForm()
    
    return render(request, 'make_appointment.html', {'form': form})

@login_required
def update_appointment(request, appointment_id):
    # Récupérer le rendez-vous associé à ce patient
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            # Sauvegarder les modifications du rendez-vous
            form.save()

            # Envoi de l'e-mail de confirmation après mise à jour
            subject = 'Votre rendez-vous a été modifié'
            message = f'Bonjour {request.user.first_name},\n\nVotre rendez-vous a été modifié avec succès pour le {appointment.date}.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]  # Email du patient

            send_mail(subject, message, from_email, recipient_list)

            # Message de succès
            messages.success(request, "Rendez-vous modifié avec succès.")
            return redirect('appointment_list')  # Redirige vers la liste des rendez-vous
        else:
            messages.error(request, "Une erreur s'est produite. Veuillez vérifier les champs.")
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'update_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointment_list.html', {'appointments': appointments})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Le rendez-vous a été supprimé avec succès.")
    return redirect('list_appointments')  # Remplacez par le nom de votre vue de liste.

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def send_confirmation_email(request):
    # Contenu de l'e-mail
    subject = 'Confirmation de votre rendez-vous'
    message = 'Votre rendez-vous a été confirmé avec succès.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['destinataire@example.com']  # Liste des destinataires

    # Envoi de l'e-mail
    send_mail(subject, message, from_email, recipient_list)
    
    return HttpResponse('E-mail envoyé avec succès !')
