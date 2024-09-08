from django.urls import path
from django.views.generic import TemplateView
from . import views  # Εισάγουμε όλες τις views από το views.py

urlpatterns = [
    path('', views.index, name='index'),
    path('ypersyndesmos/', views.ypersyndesmos_view, name='ypersyndesmos'),
    path('anafora_aks_ipiresias/', views.anafora_aks_ipiresias, name='anafora_aks_ipiresias'),
    path('epilochias/', views.epilochias_view, name='epilochias'),
    path('anafora_ipiresia/', views.anafora_ipiresia_view, name='anafora_ipiresia'),
    path('print_anafora/', views.anafora_ipiresia_view, name='print_anafora'),
    path('katalogoi/', views.katalogoi_view, name='katalogoi'),
    path('odigies_sistimaton/', views.odigies_sistimaton_view, name='odigies_sistimaton'),
    path('anafora_ipiresia_opliti/', views.anafora_ipiresia_opliti_view, name='anafora_ipiresia_opliti'),
    path('vtc/', views.vtc_view, name='vtc'),
    path('pyrseia/', views.pyrseia_view, name='pyrseia'),
    path('dides/', views.dides_view, name='dides'),
    path('katastaseis/', views.katastaseis_view, name='katastaseis'),
    path('posta/', views.posta_view, name='posta'),
]
