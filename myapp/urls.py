from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ypersyndesmos/', views.ypersyndesmos_view, name='ypersyndesmos'),
    path('anafora_aks_ipiresias/', views.anafora_aks_ipiresias, name='anafora_aks_ipiresias'),
    path('epilochias/', views.epilochias_view, name='epilochias'),
    path('anafora_ipiresia/', views.anafora_ipiresia_view, name='anafora_ipiresia'),
    path('print_anafora/', views.anafora_ipiresia_view, name='print_anafora'),  # Διόρθωση του ονόματος της view
    path('katalogoi/', views.katalogoi_view, name='katalogoi'),
]
