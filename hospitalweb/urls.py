"""
URL configuration for hospitalweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from personnel import views as pv
from patient import views
from patient.views import custom_dashboard

from appointment import views as va
from facture import views as fa
from dossiermedical import views as vd
from facture import views as fa
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from hospitalweb.admin import custom_admin_site, CustomAdminLoginView
from hospitalweb.views import custom_dashboard
from urgence import views as urgence_views
urlpatterns = [
    path('admin/login/', CustomAdminLoginView.as_view(), name='admin_login'),  # Custom login
    path('admin/', custom_admin_site.urls),
    path('personnel/', include('personnel.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Connexion via votre propre vue
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    # Ajoutez cette ligne pour la connexion via reconnaissance faciale
    path('face-login/', views.face_login, name='face_login'), 

    # Autres URL de l'application
    path('ajouter-dossier/', vd.ajouter_dossier_medical, name='ajouter_dossier_medical'),
    path('rendez-vous/', va.make_appointment, name='make_appointment'),
    path('appointment/update/<int:appointment_id>/', va.update_appointment, name='update_appointment'),
    path('appointment/', va.appointment_list, name='appointment_list'),
    path('facture/', fa.facture_list, name='facture_list'),
    path('appointment/<int:appointment_id>/delete/', va.delete_appointment, name='delete_appointment'),
    path('update/', views.update_patient, name='update_patient'),
    path('facture/pdf/<int:facture_id>/', fa.generate_pdf, name='generate_pdf'),
    
    path('delete/', views.delete_patient, name='delete_patient'),
    path('results/', views.model_results_view, name='model_results_view'),
    path('download-report/', views.download_report, name='download_report'),

    path('admin/custom-dashboard/', custom_dashboard, name='custom_dashboard'),  # Custom dashboard URL

    path('send_emergency_alert/',views.send_emergency_alert,name='send_emergency_alert'),
    path('fetch_emergencies/', urgence_views.fetch_emergencies, name='fetch_emergencies'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)