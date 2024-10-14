# myapp/urls.py
from django.urls import path, include
from django.contrib.auth.views import LoginView
from . import views  # Εισάγουμε όλες τις views από το views.py

urlpatterns = [
    # Διαδρομή για τη σελίδα σύνδεσης
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Προσθήκη της διαδρομής αποσύνδεσης

    # Αρχική σελίδα (μετά τη σύνδεση)
    path('', views.index, name='index'),

    # Άλλες διαδρομές της εφαρμογής σας
    path('index/', views.index, name='index'),
    path('ypersyndesmos/', views.ypersyndesmos_view, name='ypersyndesmos'),
    path('anafora_aks_ipiresias/', views.anafora_aks_ipiresias, name='anafora_aks_ipiresias'),
    path('epilochias/', views.epilochias_view, name='epilochias'),
    path('anafora_ipiresia/', views.anafora_ipiresia_view, name='anafora_ipiresia'),
    path('print_anafora/', views.anafora_ipiresia_view, name='print_anafora'),
    path('katalogoi/', views.katalogoi_view, name='katalogoi'),
    path('odigies_sistimaton/', views.odigies_sistimaton_view, name='odigies_sistimaton'),
    path('anafora_ipiresia_opliti/', views.anafora_ipiresia_opliti_view, name='anafora_ipiresia_opliti'),
    path('vtc/', views.vtc_view, name='vtc'),
    path('adme/', views.adme_view, name='adme'),
    path('pyrseia/', views.pyrseia_view, name='pyrseia'),
    path('dides/', views.dides_view, name='dides'),
    path('harp/', views.harp_view, name='harp'),
    path('katastaseis/', views.katastaseis_view, name='katastaseis'),
    path('posta/', views.posta_view, name='posta'),
    path('print_posta/', views.print_posta_view, name='print_posta_view'),
    path('passwords/', views.passwords_view, name='passwords_view'),
    path('exodoxarta/', views.exodoxarta_view, name='exodoxarta'),
    path('test-exodocharta/', views.test_exodocharta_view, name='test_exodocharta'),
    path('yphresiaka/', views.yphresiaka_view, name='yphresiaka'),
    path('test-yphresiaka/', views.test_yphresiaka_view, name='test_yphresiaka'),
    path('adeioxarta/', views.adeioxarta_view, name='adeioxarta'),
    path('test_adeioxarta/', views.test_adeioxarta_view, name='test_adeioxarta'),

    path('strdb/', views.strdb_view, name='strdb'),
    path('api/get_table_data/', views.get_table_data, name='get_table_data'),
    path('api/save_daily_service/', views.save_daily_service, name='save_daily_service'),
]
