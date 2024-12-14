import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from django.db.models import Sum
import json
from django.db.models import Count
from django.template.loader import render_to_string
import io
from facture.forms import FactureForm
from django.db.models import Count, Avg
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

def buffer_to_base64(buffer):
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

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
    
    def view_factures(self, request):
        factures = Facture.objects.all()
        return render(request, 'admin/all_factures_list.html', {'factures': factures})
        
    def edit_facture(self, request, facture_id):
        facture = get_object_or_404(Facture, id=facture_id)
        
        if request.method == 'POST':
            form = FactureForm(request.POST, instance=facture)  # Use the correct form class
            if form.is_valid():
                form.save()
                return redirect('/admin/factures')  # Redirect after saving
            else:
                print(form.errors)  # Debugging: Log any form validation errors
        else:
            form = FactureForm(instance=facture)  # Use FactureForm here as well

        return render(request, 'admin/edit_facture.html', {'form': form, 'facture': facture})
    
    def delete_facture(self,request, facture_id):
      facture = get_object_or_404(Facture, id=facture_id)
      facture.delete()
      return redirect('/admin/factures') 
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
        path('activity/', self.activity_page, name='activity_page'),
        path('factures/', self.view_factures, name='all_factures_list'),
        path('factures/edit/<int:facture_id>/', self.admin_view(self.edit_facture), name='edit_facture'),
        path('factures/delete/<int:facture_id>/', self.admin_view(self.delete_facture), name='delete_facture'),
      ]
      return custom_urls + urls

 #    def activity_page(self, request):
    #       return render(request, 'admin/activity_page.html', {})
    def activity_page(self, request):
        # Gender distribution
        gender_distribution = CustomUser.objects.values('gender').annotate(count=Count('id'))
        male_count = sum(item['count'] for item in gender_distribution if item['gender'] == 'Male')
        female_count = sum(item['count'] for item in gender_distribution if item['gender'] == 'Female')
        total_patients = male_count + female_count
        male_percentage = (male_count / total_patients * 100) if total_patients else 0
        female_percentage = (female_count / total_patients * 100) if total_patients else 0
        print("Gender Data:", total_patients)

        # Patient Status Distribution
        status_distribution = CustomUser.objects.values('status').annotate(count=Count('id'))

        # Age Distribution
        average_age = CustomUser.objects.aggregate(avg_age=Avg('age'))['avg_age']
        age_ranges = {
            'Below 20': CustomUser.objects.filter(age__lt=20).count(),
            '20-40': CustomUser.objects.filter(age__gte=20, age__lt=40).count(),
            '40-60': CustomUser.objects.filter(age__gte=40, age__lt=60).count(),
            'Above 60': CustomUser.objects.filter(age__gte=60).count(),
        }

        # Emergency Cases
        emergency_case_count = CustomUser.objects.filter(emergency_case=True).count()
        print("Emergency case count:", emergency_case_count)

        # Generate charts
        gender_chart_image = self.generate_gender_chart(male_percentage, female_percentage)
        status_chart_image = self.generate_status_chart(status_distribution)
        age_chart_image = self.generate_age_chart(age_ranges)

        # Query facture data: total amounts per month
        factures = Facture.objects.values('date_emission__month', 'date_emission__year') \
            .annotate(total_amount=Sum('montant')) \
            .order_by('date_emission__year', 'date_emission__month')

        # For the chart data
        if factures.exists():
            months = [
                f"{facture['date_emission__year']}-{facture['date_emission__month']:02d}"
                for facture in factures
            ]
            totals = [facture['total_amount'] for facture in factures]
        else:
            months = ["No Data"]
            totals = [0]

        # Query for paid and unpaid invoices for a pie chart
        payment_status = Facture.objects.values('est_payee').annotate(count=Count('id'))

        paid = next((item['count'] for item in payment_status if item['est_payee']), 0)
        unpaid = next((item['count'] for item in payment_status if not item['est_payee']), 0)

        # Handle case with no invoices
        if paid == 0 and unpaid == 0:
            paid, unpaid = 1, 0  # To avoid pie chart rendering issues with zero total

        # Generate the charts as images
        facture_chart_image = self.generate_facture_chart(months, totals)
        payment_chart_image = self.generate_payment_chart(paid, unpaid)
        # Appointment Distribution by Month


        appointment_distribution = Appointment.objects.values('date__month', 'date__year') \
            .annotate(appointment_count=Count('id')) \
            .order_by('date__year', 'date__month')

        # Prepare data for the chart
        months = [f"{appointment['date__year']}-{appointment['date__month']:02d}" for appointment in appointment_distribution]
        counts = [appointment['appointment_count'] for appointment in appointment_distribution]

        # Generate appointment chart image
        appointment_chart_image = self.generate_appointment_chart(months, counts)

        # Prepare context for the template
        context = {
            'gender_chart_image': gender_chart_image,
            'status_chart_image': status_chart_image,
            'age_chart_image': age_chart_image,
            'average_age': average_age,
            'emergency_case_count': emergency_case_count,
            'facture_chart_image': facture_chart_image,
            'payment_chart_image': payment_chart_image,
            'appointment_chart_image': appointment_chart_image,  # Add appointment chart to context

        }

        return render(request, 'admin/activity_page.html', context)
    
    def generate_appointment_chart(self, months, counts):
        """Generate the appointment distribution chart as an image."""
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(months, counts, color='#FF5733', edgecolor='#C70039')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Appointments')
        ax.set_title('Appointments Distribution by Month')
        ax.tick_params(axis='x', rotation=90)  # Rotate x-axis labels to avoid overlap

        # Save the chart as an image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = buffer_to_base64(buffer)
        plt.close()  # Avoid memory leaks
        return base64_image


    def generate_gender_chart(self, male_percentage, female_percentage):
        """Generate gender distribution chart."""
        fig, ax = plt.subplots(figsize=(6, 6))
        labels = ['Male', 'Female']
        values = [male_percentage, female_percentage]
        ax.pie(values, labels=labels, colors=['#007BFF', '#FFC0CB'], autopct='%1.1f%%')
        ax.set_title('Gender Distribution')

        # Save chart as an image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = buffer_to_base64(buffer)
        plt.close()
        return base64_image

    def generate_status_chart(self, status_distribution):
        """Generate patient status distribution chart."""
        fig, ax = plt.subplots(figsize=(8, 4))
        statuses = [item['status'] for item in status_distribution]
        counts = [item['count'] for item in status_distribution]
        ax.bar(statuses, counts, color='#28A74580', edgecolor='#28A745')
        ax.set_xlabel('Status')
        ax.set_ylabel('Count')
        ax.set_title('Patient Status Distribution')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = buffer_to_base64(buffer)
        plt.close()
        return base64_image

    def generate_age_chart(self, age_ranges):
        """Generate age distribution chart."""
        fig, ax = plt.subplots(figsize=(8, 4))
        ranges = list(age_ranges.keys())
        counts = list(age_ranges.values())
        ax.bar(ranges, counts, color='#FF573380', edgecolor='#FF5733')
        ax.set_xlabel('Age Range')
        ax.set_ylabel('Count')
        ax.set_title('Age Distribution')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = buffer_to_base64(buffer)
        plt.close()
        return base64_image


    def generate_facture_chart(self, labels, data):
        """Generate the facture chart as an image."""
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, data, color='#007BFF80', edgecolor='#007BFF')
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Facture Amount (in USD)')
        ax.set_title('Total Amounts by Month')
        ax.tick_params(axis='x', rotation=90)

        # Save the chart as an image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = buffer_to_base64(buffer)
        plt.close()  # Avoid memory leaks
        return base64_image


    def generate_payment_chart(self, paid, unpaid):
        """Generate the payment status chart as an image."""
        fig, ax = plt.subplots(figsize=(6, 6))
        labels = ['Paid', 'Unpaid']
        values = [paid, unpaid]
        ax.pie(values, labels=labels, colors=['#28a745', '#dc3545'], autopct='%1.1f%%')
        ax.set_title('Paid vs Unpaid Invoices')

        # Save the chart as an image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        base64_image = buffer_to_base64(buffer)
        plt.close()  # Avoid memory leaks
        return base64_image

custom_admin_site = CustomAdminSite(name='custom_admin')