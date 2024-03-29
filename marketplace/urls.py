"""
URL configuration for Asignatura_VyV_2023B project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from marketplace import views

urlpatterns = [
    path('', views.index),
    path('seguimiento_entrega/<int:vendedor_id>', views.seguimiento_entrega, name='seguimiento_entrega'),
    path('seguimientoInterno', views.seguimiento_interno),
    path('feedback/', views.feedback, name='feedback'),
    path('metrica/<int:vendedor_id>/', views.metricas),
    path('buscar_producto/', views.buscar_producto,name='buscar_producto'),
]
