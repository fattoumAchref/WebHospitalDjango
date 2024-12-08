from django.contrib import admin
from django.shortcuts import render,redirect
from personnel.models import Personnel
from patient.models import CustomUser
from appointment.models import Appointment
from dossiermedical.models import DossierMedical
from facture.models import Facture
from django import forms
from django.contrib import messages
from django.urls import path
from django.contrib.auth import logout,login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from datetime import date,timedelta,datetime, timezone
import csv
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def get_total_appointments():
    return Appointment.objects.count()

def get_appointment_percentage_change():
    last_month_date = date.today() - timedelta(days=30)
    total_appointments_last_month = Appointment.objects.filter(date__lt=last_month_date).count()
    total_appointments = Appointment.objects.count()
    if total_appointments_last_month > 0:
        return ((total_appointments - total_appointments_last_month) / total_appointments_last_month) * 100
    return 0 

def get_appointment_increase():
    last_month_date = date.today() - timedelta(days=30)
    return Appointment.objects.filter(date__gte=last_month_date).count()

def get_appointment_decrease():
    last_month_date = date.today() - timedelta(days=30)
    return Appointment.objects.filter(date__lte=last_month_date).count()

def get_total_doctors():
    return Personnel.objects.count()

def get_doctor_percentage_change():
    last_month_date = date.today() - timedelta(days=30)
    total_doctors_last_month = Personnel.objects.filter(date_joined__lt=last_month_date).count()
    total_doctors = get_total_doctors()
    if total_doctors_last_month > 0:
        return ((total_doctors - total_doctors_last_month) / total_doctors_last_month) * 100
    return 0

def get_doctor_increase():
    last_month_date = date.today() - timedelta(days=30)
    return Personnel.objects.filter(date_joined__gte=last_month_date).count()

def get_doctor_decrease():
   last_month_date = date.today() - timedelta(days=30)
   return Personnel.objects.filter(date_left__gte=last_month_date).count() 

def get_total_patients():
    return CustomUser.objects.filter().count()

def get_patient_percentage_change():
    last_month_date = date.today() - timedelta(days=1)
    active_patients_last_month = CustomUser.objects.filter(
     date_joined__lt=last_month_date
    ).count()
    active_patients = get_total_patients()
    if active_patients_last_month > 0:
        percentage_change = ((active_patients - active_patients_last_month) / active_patients_last_month) * 100
        return int(percentage_change)
    return 0

def get_patient_increase():
    today_start = datetime.combine(date.today(), datetime.min.time())
    return CustomUser.objects.filter(date_joined__gte=today_start).count()

def get_patient_decrease():
    today_start = datetime.combine(date.today(), datetime.min.time())
    return CustomUser.objects.filter(is_active=False, date_left__gte=today_start).count()

def mark_patient_as_left(patient_id):
    try:
        patient = CustomUser.objects.get(id=patient_id)
        patient.date_left = timezone.now()
        patient.save()
        print(f"Updated date_left for {patient.username}: {patient.date_left}")
    except CustomUser.DoesNotExist:
        print(f"Patient with ID {patient_id} not found.")

def get_total_emergency_cases():
    return CustomUser.objects.filter(emergency_case=True).count()

# Calculate the percentage change in emergency cases
def get_emergency_case_percentage_change():
    last_month_date = date.today() - timedelta(days=30)
    emergency_cases_last_month = CustomUser.objects.filter(
        emergency_case=True, date_joined__lt=last_month_date
    ).count()
    current_emergency_cases = CustomUser.objects.filter(emergency_case=True).count()
    if emergency_cases_last_month > 0:
        return ((current_emergency_cases - emergency_cases_last_month) / emergency_cases_last_month) * 100
    return 0

# Count the new emergency cases in the last month
def get_emergency_case_increase():
    last_month_date = date.today() - timedelta(days=30)
    return CustomUser.objects.filter(emergency_case=True, date_joined__gte=last_month_date).count()

# Count the emergency cases resolved in the last month
def get_emergency_case_decrease():
    last_month_date = date.today() - timedelta(days=30)
    return CustomUser.objects.filter(emergency_case=True, date_left__gte=last_month_date).count()

class CustomAdminLoginView(LoginView):
    template_name = 'admin/custom_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return HttpResponseRedirect('/admin/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Authenticate and log the user in
        user = form.get_user()
        login(self.request, user)
        if not user.is_staff:
            logout(self.request)
            messages.error(self.request, "You are not authorized to access the admin site.")
            return self.form_invalid(form) 
        next_url = self.request.GET.get('next', '/admin/')
        return HttpResponseRedirect(next_url)

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ['nom', 'prenom', 'fonction', 'telephone', 'email', 'adresse', 'photo']
        widgets = {
            'fonction': forms.Select(attrs={'class': 'form-control'},choices=Personnel.FONCTION_CHOICES),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class PatientForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'phone_number', 'status', 'is_active', 'age','date_joined','is_staff']
        widgets = {
            'date_joined': forms.DateInput(attrs={'class': 'form-control'}),
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control'}),  
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    personnel = forms.ModelChoiceField(
        queryset=Personnel.objects.all(),
        required=True,
        label="Choisir un personnel",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'description', 'personnel']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'personnel': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomAdminSite(admin.AdminSite):
    site_header = "My Custom Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to My Admin"
    login_url = '/admin/login/'

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_staff

    def index(self, request, extra_context=None):
        # Redirect to login page if the user lacks permissions
        if not request.user.is_authenticated:
         return HttpResponseRedirect(self.login_url)
    
        extra_context = extra_context or {}
        extra_context['custom_dashboard_url'] = reverse('custom_dashboard') 

        extra_context['total_doctors'] = get_total_doctors() 

        total_patients = CustomUser.objects.count()
        extra_context['total_patients'] = total_patients

        extra_context['total_appointments'] = get_total_appointments()

          # Handle patient deletion
        if request.method == "POST" and "delete_patient" in request.POST:
          patient_id = request.POST.get("delete_patient")
          try:
            patient = get_object_or_404(CustomUser, id=patient_id)
            patient_name = f"{patient.first_name} {patient.last_name}" if patient.first_name and patient.last_name else "Unknown"
            mark_patient_as_left(patient_id)
            patient.delete()
            messages.success(request, f"Patient {patient_name} deleted successfully!")
          except Exception as e:
            messages.error(request, f"An error occurred while deleting the patient: {str(e)}")
        
          # Handle doctor deletion
        if request.method == "POST" and "delete_doctor" in request.POST:
          doctor_id = request.POST.get("delete_doctor")
          try:
            doctor = get_object_or_404(Personnel, id=doctor_id)
            doctor_name = f"{doctor.nom} {doctor.prenom}" if doctor.nom and doctor.prenom else "Unknown"
            doctor.delete()
            messages.success(request, f"Doctor {doctor_name} deleted successfully!")
          except Exception as e:
            messages.error(request, f"An error occurred while deleting the doctor: {str(e)}")

        patients = CustomUser.objects.all()
        extra_context['patients'] = patients

        selected_fonction = request.GET.get('fonction', '')

        if selected_fonction:
          doctors = Personnel.objects.filter(fonction=selected_fonction)
        else:
          doctors = Personnel.objects.filter(fonction__startswith='Médecin')

        extra_context['doctors'] = doctors
        extra_context['selected_fonction'] = selected_fonction 

        extra_context['emergency_cases'] = get_total_emergency_cases()

        extra_context['doctor_percentage_change'] = get_doctor_percentage_change()
        extra_context['doctor_increase'] = get_doctor_increase()
        extra_context['doctor_decrease'] = get_doctor_decrease()

        extra_context['patient_percentage_change'] = get_patient_percentage_change()
        extra_context['patient_increase'] = get_patient_increase()
        extra_context['patient_decrease'] = get_patient_decrease()

        extra_context['appointment_percentage_change'] = get_appointment_percentage_change()
        extra_context['appointment_decrease'] = get_appointment_decrease()
        extra_context['appointment_increase'] = get_appointment_increase()

        extra_context['emergency_case_percentage_change'] = get_emergency_case_percentage_change()
        extra_context['emergency_case_increase'] = get_emergency_case_increase()
        extra_context['emergency_case_decrease'] = get_emergency_case_decrease()

        return super().index(request, extra_context) 
            
    def add_doctor_view(self, request):
        if not request.user.is_staff:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('/admin') 
        
        if request.method == 'POST':
           form = DoctorForm(request.POST, request.FILES)
           if form.is_valid():
               form.save()
               messages.success(request, "Doctor added successfully!")
               return redirect('/admin')
        else:
            form = DoctorForm() 
        return render(request, 'admin/add_doctor.html', {'form': form})
    
    def add_patient_view(self, request):
        if not request.user.is_staff:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('/admin')
        
        if request.method == 'POST':
           form = PatientForm(request.POST, request.FILES)
           if form.is_valid():
               form.save()
               messages.success(request, "Patient added successfully!")
               return redirect('/admin') 
        else:
            form = PatientForm() 
        print(form) 
        return render(request, 'admin/add_patient.html', {'form': form})
    
    def edit_patient(self, request, patient_id):
        patient = get_object_or_404(CustomUser, id=patient_id)
        if request.method == 'POST':
            form = PatientForm(request.POST, request.FILES, instance=patient)
            if form.is_valid():
                form.save()
                return redirect('/admin') 
        else:
            form = PatientForm(instance=patient)
        return render(request, 'admin/edit_patient.html', {'form': form,'patient':patient})
    
    def edit_doctor(self, request, doctor_id):
       doctor = get_object_or_404(Personnel, id=doctor_id)
       if request.method == "POST":
           form = DoctorForm(request.POST, request.FILES, instance=doctor)
           if form.is_valid():
               form.save()
               return redirect('admin:index') 
       else:
           form = DoctorForm(instance=doctor)
       return render(request, 'admin/edit_doctor.html', {'form': form,'doctor':doctor}) 
    
    def delete_doctor(self,request, doctor_id):
      doctor = get_object_or_404(Personnel, id=doctor_id)
      doctor.delete()
      return redirect('admin:index')
    
    def delete_patient(self,request, patient_id):
      patient = get_object_or_404(CustomUser, id=patient_id)
      patient.delete()
      return redirect('admin:index')
     
    def view_appointments(self, request):
        appointments = Appointment.objects.all()
        return render(request, 'admin/all_appointments_list.html', {'appointments': appointments})
    
    def view_patients(self,request):
        patients = CustomUser.objects.all()
        return render(request,'admin/all_patients_list.html',{'patients' : patients})
    
       
    def edit_appointment(self,request, appointment_id):
       appointment = get_object_or_404(Appointment, id=appointment_id)
    
       if request.method == 'POST':
           form = AppointmentForm(request.POST, instance=appointment)
           if form.is_valid():
               form.save()
               return redirect('/admin/appointments') 
       else:
           form = AppointmentForm(instance=appointment)

       return render(request, 'admin/edit_appointment.html', {'form': form, 'appointment': appointment})  
    
    def delete_appointment(self,request, appointment_id):
      appointment = get_object_or_404(Appointment, id=appointment_id)
      appointment.delete()
      return redirect('/admin/appointments') 
    
    def export_patients_csv(self, request):
        patients = CustomUser.objects.all()

        # Create the HttpResponse object with CSV headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="patients.csv"'

        # Write CSV data
        writer = csv.writer(response)
        writer.writerow(['username','first_name', 'last_name', 'email', 'phone_number', 'status', 'is_active', 'age','date_joined','is_staff'])
        for patient in patients:
            writer.writerow([patient.username, patient.first_name, patient.last_name, patient.email, patient.phone_number, patient.is_active, patient.age, patient.date_joined, patient.is_staff])
        return response
    
    def export_pdf_dossier_medical(self,request, patient_id):
      patient = CustomUser.objects.get(id=patient_id)
      context = {
        'patient': patient
      }
      template = get_template('admin/patient_dossier_pdf.html')
      html = template.render(context)

      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = f'attachment; filename="patient_{patient_id}_dossier.pdf"'

      pisa_status = pisa.CreatePDF(html, dest=response)

      if pisa_status.err:
        return HttpResponse('Error generating PDF')

      return response

    def get_urls(self):
      urls = super().get_urls()
      custom_urls = [
        path('add-doctor/', self.admin_view(self.add_doctor_view), name='add_doctor'),
        path('add-patient/', self.admin_view(self.add_patient_view), name='add_patient'),
        path('dossier-medical/<int:patient_id>/pdf/', self.admin_view(self.export_pdf_dossier_medical), name='export_pdf_dossier_medical'),
        path('edit-patient/<int:patient_id>/', self.admin_view(self.edit_patient), name='edit_patient'),
        path('doctor/edit/<int:doctor_id>/', self.admin_view(self.edit_doctor), name='edit_doctor'),
        path('doctor/delete/<int:doctor_id>/', self.admin_view(self.delete_doctor), name='delete_doctor'),
        path('patient/delete/<int:patient_id>/', self.admin_view(self.delete_patient), name='delete_patient'),
        path('appointments/', self.view_appointments, name='all_appointments_list'),
        path('patients/', self.view_patients, name='all_patients_list'),
        path('appointment/edit/<int:appointment_id>/', self.admin_view(self.edit_appointment), name='edit_appointment'),
        path('appointment/delete/<int:appointment_id>/', self.admin_view(self.delete_appointment), name='delete_appointment'),
        path('export-patients-csv/', self.admin_view(self.export_patients_csv), name='export-patients-csv'),
      ]
      return custom_urls + urls

custom_admin_site = CustomAdminSite(name='custom_admin')