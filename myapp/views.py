from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import DidesCategory, HarpCategory, AdmeCategory, OfficerServiceReport, Soldier, AxypKepikServiceReport
from django.core.files.base import ContentFile
from django.http import HttpResponse
from io import BytesIO
import pdfkit
import tempfile
from datetime import datetime
from django.utils.translation import gettext as _
from django.utils.formats import date_format
import locale
import os

def index(request):
    return render(request, 'index.html')

def ypersyndesmos_view(request):
    unclassified_network = DidesCategory.objects.filter(category='unclassified')
    classified_network = DidesCategory.objects.filter(category='classified')
    harp_categories = HarpCategory.objects.all()
    adme_categories = AdmeCategory.objects.all()
    
    context = {
        'unclassified_network': unclassified_network,
        'classified_network': classified_network,
        'harp_categories': harp_categories,
        'adme_categories': adme_categories,
    }
    
    return render(request, 'ypersyndesmos.html', context)

def anafora_aks_ipiresias(request):
    return render(request, 'anafora_aks_ipiresias.html')

def epilochias_view(request):
    return render(request, 'epilochias.html')

def anafora_ipiresia_view(request):
    if request.method == 'POST':
        # Παίρνουμε την ημερομηνία από το request
        report_date = request.POST.get('report_date')
        
        # Μετατροπή της ημερομηνίας στο format dd/mm/yyyy
        formatted_date = datetime.strptime(report_date, '%Y-%m-%d').strftime('%d/%m/%Y')
            
        context = {
            'officer': OfficerServiceReport.objects.get(id=request.POST.get('officer')),
            'info_kepik': request.POST.get('info_kepik'),
            'info_lohos': request.POST.get('info_lohos'),
            'info_monada': request.POST.get('info_monada'),
            'keys': request.POST.get('keys'),
            'tele_center': Soldier.objects.get(id=request.POST.get('tele_center')),
            'phone_check': request.POST.get('phone_check'),
            'interrupts': request.POST.get('interrupts'),
            'causes': request.POST.get('causes'),
            'actions': request.POST.get('actions'),
            'restored': request.POST.get('restored'),
            'tele_register': Soldier.objects.get(id=request.POST.get('tele_register')),
            'system_sda': request.POST.get('system_sda'),
            'system_aifs': request.POST.get('system_aifs'),
            'system_cronos': request.POST.get('system_cronos'),
            'system_faults': request.POST.get('system_faults'),
            'repair_actions': request.POST.get('repair_actions'),
            'harp_phone': request.POST.get('harp_phone'),
            'vpn_check': request.POST.get('vpn_check'),
            'trackharp_check': request.POST.get('trackharp_check'),
            'network_check': request.POST.get('network_check'),
            'network_problem': request.POST.get('network_problem'),
            'server_check': request.POST.get('server_check'),
            'server_problem': request.POST.get('server_problem'),
            'application_check': request.POST.get('application_check'),
            'vosip_check': request.POST.get('vosip_check'),
            'vosip_problem': request.POST.get('vosip_problem'),
            'circuit_routing': request.POST.get('circuit_routing'),
            'application_served': request.POST.get('application_served'),
            'ote_fault_number': request.POST.get('ote_fault_number'),
            'outage_duration': request.POST.get('outage_duration'),
            'alternative_routing': request.POST.get('alternative_routing'),
            'microwave_check': request.POST.get('microwave_check'),
            'eseetha_fault_signal': request.POST.get('eseetha_fault_signal'),
            'satellite_check': request.POST.get('satellite_check'),
            'satellite_faults': request.POST.get('satellite_faults'),
            'pyrseia_status': request.POST.get('pyrseia_status'),
            'cleaning_done': request.POST.get('cleaning_done'),
            'commander_informed': request.POST.get('commander_informed'),
            'observations': request.POST.get('observations'),
            'commander_kepik': OfficerServiceReport.objects.get(id=request.POST.get('commander_kepik')),
            'officer_duty': OfficerServiceReport.objects.get(id=request.POST.get('officer_duty')),
            'commander': OfficerServiceReport.objects.get(id=request.POST.get('commander')),
            'formatted_date': formatted_date,  # Προσθήκη της μορφοποιημένης ημερομηνίας στο context

        }

        # Δημιουργία του HTML από το template
        html_string = render_to_string('print_anafora.html', context)

        # Αποθήκευση του HTML σε προσωρινό αρχείο
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_html_file:
            temp_html_file.write(html_string.encode('utf-8'))
            temp_html_file_path = temp_html_file.name

        # Διαμόρφωση του pdfkit με το μονοπάτι του εκτελέσιμου wkhtmltopdf
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=os.path.join('myapp', 'bin', 'wkhtmltopdf.exe'))

        # Δημιουργία του PDF από το προσωρινό αρχείο με επιπλέον options
        pdf = pdfkit.from_file(temp_html_file_path, False, configuration=pdfkit_config, options={
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',  # Αυτό επιτρέπει την πρόσβαση σε τοπικά αρχεία
            'orientation': 'Landscape'  # Καθορίζει την οριζόντια εκτύπωση
        })

        # Αποθήκευση του PDF στο μοντέλο
        service_report = AxypKepikServiceReport()
        service_report.pdf.save('Αναφορά_ΑΞΥΠ_{}.pdf'.format(datetime.now().strftime('%d-%m-%Y')), ContentFile(pdf))

        # Ανακατεύθυνση ή εμφάνιση της σελίδας με το PDF
        return HttpResponse(pdf, content_type='application/pdf')

    # Εμφάνιση της φόρμας για συμπλήρωση
    officers = OfficerServiceReport.objects.all()
    soldiers = Soldier.objects.all()
    return render(request, 'anafora_ipiresia.html', {'officers': officers, 'soldiers': soldiers})

def katalogoi_view(request):
    return render(request, 'katalogoi.html')

def odigies_sistimaton_view(request):
    return render(request, 'odigies_sistimaton.html')

def anafora_ipiresia_opliti_view(request):
    if request.method == 'POST':
        context = {
            'report_date': request.POST.get('report_date'),
            'arrival_time': request.POST.get('arrival_time'),
            'departure_time': request.POST.get('departure_time'),
            'problems': request.POST.get('problems'),
            'incoming_signals': request.POST.get('incoming_signals'),
            'outgoing_signals': request.POST.get('outgoing_signals'),
            'transit_signals': request.POST.get('transit_signals'),
            'non_transmitted_signals': request.POST.get('non_transmitted_signals'),
            'system_operation': request.POST.get('system_operation'),
            'transmission_issues': request.POST.get('transmission_issues'),
            'cronos_signals': request.POST.get('cronos_signals'),
            'cronos_non_transmitted': request.POST.get('cronos_non_transmitted'),
            'cronos_system_operation': request.POST.get('cronos_system_operation'),
            'cronos_issues': request.POST.get('cronos_issues'),
            'aifs_signals': request.POST.get('aifs_signals'),
            'aifs_non_transmitted': request.POST.get('aifs_non_transmitted'),
            'aifs_system_operation': request.POST.get('aifs_system_operation'),
            'aifs_issues': request.POST.get('aifs_issues'),
            'general_observations': request.POST.get('general_observations')
        }

    context = {
        'range_0_10': range(11),  # για drop-down λίστες με επιλογές 0-10
        'range_0_21': range(22),  # για drop-down λίστες με επιλογές 0-21
        'range_0_41': range(42),  # για drop-down λίστες με επιλογές 0-41
    }
    
    return render(request, 'anafora_ipiresia_opliti.html')
