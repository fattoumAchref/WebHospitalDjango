from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from .forms import PatientUpdateForm
from django.contrib.auth.decorators import login_required
from personnel.models import Personnel
from django.contrib.admin.views.decorators import staff_member_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('login')  # Redirige vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Erreur lors de la saisie. Veuillez réessayer.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    doctors=Personnel.objects.filter(fonction__startswith="Médecin")
    return render(request, 'index.html',{'doctors':doctors})

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')


@login_required
def update_patient(request):
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont étées mises à jour avec succès.")
            return redirect('update_patient')
    else:
        form = PatientUpdateForm(instance=request.user)
    
    return render(request, 'modif_patient.html', {'form': form})

@login_required
def delete_patient(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Votre compte a été supprimé avec succès.")
        
        return redirect('home')
    return render(request, 'delete_patient.html')

@staff_member_required
def custom_dashboard(request):
    return HttpResponse("<h1>Welcome to the Custom Dashboard</h1>")