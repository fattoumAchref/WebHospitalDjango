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
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Link to the logged-in patient
            appointment.save()
            messages.success(request, "Votre rendez-vous a été pris avec succès.")
            return redirect('home')
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
            form.save()
            messages.success(request, "Rendez-vous modifié avec succès.")
            return redirect('appointment_list')  # Rediriger vers la liste des rendez-vous
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