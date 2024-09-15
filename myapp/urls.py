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
    path('print_posta/', views.print_posta_view, name='print_posta_view'),
    path('passwords/', views.passwords_view, name='passwords_view'),  # Προσθήκη του νέου URL για το passwords_view
    path('exodoxarta/', views.exodoxarta_view, name='exodoxarta'),
    path('test-exodocharta/', views.test_exodocharta_view, name='test_exodocharta'),
    path('yphresiaka/', views.yphresiaka_view, name='yphresiaka'),  # Προσθήκη για το yphresiaka_view
    path('test-yphresiaka/', views.test_yphresiaka_view, name='test_yphresiaka'),  # Προσθήκη για το test_yphresiaka_view
    path('adeioxarta/', views.adeioxarta_view, name='adeioxarta'),
    path('test_adeioxarta/', views.adeioxarta_view, name='test_adeioxarta'),  # Διαδρομή για το test view
]
