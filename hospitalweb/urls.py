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
from appointment import views as va
from dossiermedical import views as vd
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('personnel/',include('personnel.urls')),
    path('home/',views.home, name='home'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('ajouter-dossier/', vd.ajouter_dossier_medical, name='ajouter_dossier_medical'),
    path('rendez-vous/', va.make_appointment, name='make_appointment'),
]
