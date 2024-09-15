from django.shortcuts import render, redirect
from django.db.models import Sum
from django.template.loader import render_to_string
from .models import DidesCategory, HarpCategory, AdmeCategory, OfficerServiceReport, Soldier, AxypKepikServiceReport, OplitiServiceReport, ServiceReportSummary, AxypCodesCategory  
from django.core.files.base import ContentFile
from django.http import HttpResponse
from io import BytesIO
import pdfkit
import tempfile
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from django.utils.formats import date_format
import locale
import os
import platform
from django.urls import reverse
from django.shortcuts import redirect
from .forms import SoldierForm, SummaryForm


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

    # Ανίχνευση του λειτουργικού συστήματος και διαμόρφωση του pdfkit
        if platform.system() == 'Windows':
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf.exe')
        elif platform.system() == 'Darwin':  # Darwin είναι το όνομα του πυρήνα του macOS
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf')
        else:
            raise Exception("Unsupported OS")

        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

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
        # Παίρνουμε την ημερομηνία από το request
        report_date = request.POST.get('report_date')
        
        # Μετατροπή της ημερομηνίας στο format dd/mm/yyyy
        formatted_date = datetime.strptime(report_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        # Παίρνουμε τα σύνολα
        total_sda = int(request.POST.get('hidden_total_sum_sda', 0))
        total_aifs = int(request.POST.get('hidden_total_sum_aifs', 0))
        total_cronos = int(request.POST.get('hidden_total_sum_cronos', 0))
        total_general = int(request.POST.get('hidden_total_sum_general', 0))

        # Αποθηκεύουμε τα σύνολα στη βάση δεδομένων
        ServiceReportSummary.objects.create(
            report_date=report_date,
            total_sda=total_sda,
            total_aifs=total_aifs,
            total_cronos=total_cronos,
            total_general=total_general
        )

        # Συλλογή των δεδομένων από τη φόρμα
        context = {
            'report_date': formatted_date,
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
            'general_observations': request.POST.get('general_observations'),
            'remarks': request.POST.get('remarks'),
            
            # Προσθήκη δεδομένων από τη φόρμα για τα πεδία που σχετίζονται με ΣΔΑ – ΠΥΡΣΕΙΑ
            'zu': request.POST.get('zu'),
            'ou': request.POST.get('ou'),
            'pu': request.POST.get('pu'),
            'ru': request.POST.get('ru'),
            'zh': request.POST.get('zh'),
            'oh': request.POST.get('oh'),
            'ph': request.POST.get('ph'),
            'rh': request.POST.get('rh'),

            # Προσθήκη δεδομένων από τη φόρμα για τα πεδία που σχετίζονται με AIFS
            'zu_aifs': request.POST.get('zu_aifs'),
            'ou_aifs': request.POST.get('ou_aifs'),
            'pu_aifs': request.POST.get('pu_aifs'),
            'ru_aifs': request.POST.get('ru_aifs'),
            'zh_aifs': request.POST.get('zh_aifs'),
            'oh_aifs': request.POST.get('oh_aifs'),
            'ph_aifs': request.POST.get('ph_aifs'),
            'rh_aifs': request.POST.get('rh_aifs'),

            # Προσθήκη δεδομένων από τη φόρμα για τα πεδία που σχετίζονται με CRONOS
            'zu_cronos': request.POST.get('zu_cronos'),
            'ou_cronos': request.POST.get('ou_cronos'),
            'pu_cronos': request.POST.get('pu_cronos'),
            'ru_cronos': request.POST.get('ru_cronos'),
            'zh_cronos': request.POST.get('zh_cronos'),
            'oh_cronos': request.POST.get('oh_cronos'),
            'ph_cronos': request.POST.get('ph_cronos'),
            'rh_cronos': request.POST.get('rh_cronos'),

            # Προσθήκη δεδομένων από τη φόρμα για τα πεδία που σχετίζονται με το γενικό σύνολο
            'zu_total': request.POST.get('zu_total'),
            'ou_total': request.POST.get('ou_total'),
            'pu_total': request.POST.get('pu_total'),
            'ru_total': request.POST.get('ru_total'),
            'zh_total': request.POST.get('zh_total'),
            'oh_total': request.POST.get('oh_total'),
            'ph_total': request.POST.get('ph_total'),
            'rh_total': request.POST.get('rh_total'),

            # Προσθήκη δεδομένων από τη φόρμα για το συνολικό σύνολο των δεδομένων
            'zu_general': request.POST.get('zu_general'),
            'ou_general': request.POST.get('ou_general'),
            'pu_general': request.POST.get('pu_general'),
            'ru_general': request.POST.get('ru_general'),
            'zh_general': request.POST.get('zh_general'),
            'oh_general': request.POST.get('oh_general'),
            'ph_general': request.POST.get('ph_general'),
            'rh_general': request.POST.get('rh_general'),
            
            'total_sum_sda': request.POST.get('total_sum_sda'),
            'total_sum_aifs': request.POST.get('total_sum_aifs'),
            'total_sum_cronos': request.POST.get('total_sum_cronos'),
            'total_sum_incoming': request.POST.get('total_sum_incoming'),
            'total_sum_general': request.POST.get('total_sum_general'),
            
            # Προσθήκη συνόλων από τα hidden fields
            'total_sum_sda': request.POST.get('hidden_total_sum_sda'),
            'total_sum_aifs': request.POST.get('hidden_total_sum_aifs'),
            'total_sum_cronos': request.POST.get('hidden_total_sum_cronos'),
            'total_sum_incoming': request.POST.get('hidden_total_sum_incoming'),
            'total_sum_general': request.POST.get('hidden_total_sum_general'),
            
            'check_1_14': request.POST.get('check_1_14'),
            'check_1_18': request.POST.get('check_1_18'),
            'check_1_23': request.POST.get('check_1_23'),
            'check_1_03': request.POST.get('check_1_03'),
            'check_1_06': request.POST.get('check_1_06'),
            'check_2_14': request.POST.get('check_2_14'),
            'check_2_18': request.POST.get('check_2_18'),
            'check_2_23': request.POST.get('check_2_23'),
            'check_2_03': request.POST.get('check_2_03'),
            'check_2_06': request.POST.get('check_2_06'),
            'check_3_14': request.POST.get('check_3_14'),
            'check_3_18': request.POST.get('check_3_18'),
            'check_3_23': request.POST.get('check_3_23'),
            'check_3_03': request.POST.get('check_3_03'),
            'check_3_06': request.POST.get('check_3_06'),
            'check_4_14': request.POST.get('check_4_14'),
            'check_4_18': request.POST.get('check_4_18'),
            'check_4_23': request.POST.get('check_4_23'),
            'check_4_03': request.POST.get('check_4_03'),
            'check_4_06': request.POST.get('check_4_06'),
            'check_5_14': request.POST.get('check_5_14'),
            'check_5_18': request.POST.get('check_5_18'),
            'check_5_23': request.POST.get('check_5_23'),
            'check_5_03': request.POST.get('check_5_03'),
            'check_5_06': request.POST.get('check_5_06'),
            'check_6_14': request.POST.get('check_6_14'),
            'check_6_18': request.POST.get('check_6_18'),
            'check_6_23': request.POST.get('check_6_23'),
            'check_6_03': request.POST.get('check_6_03'),
            'check_6_06': request.POST.get('check_6_06'),
            'check_7_14': request.POST.get('check_7_14'),
            'check_7_18': request.POST.get('check_7_18'),
            'check_7_23': request.POST.get('check_7_23'),
            'check_7_03': request.POST.get('check_7_03'),
            'check_7_06': request.POST.get('check_7_06'),
            'check_8_14': request.POST.get('check_8_14'),
            'check_8_18': request.POST.get('check_8_18'),
            'check_8_23': request.POST.get('check_8_23'),
            'check_8_03': request.POST.get('check_8_03'),
            'check_8_06': request.POST.get('check_8_06'),
            'check_9_14': request.POST.get('check_9_14'),
            'check_9_18': request.POST.get('check_9_18'),
            'check_9_23': request.POST.get('check_9_23'),
            'check_9_03': request.POST.get('check_9_03'),
            'check_9_06': request.POST.get('check_9_06'),
            'check_10_14': request.POST.get('check_10_14'),
            'check_10_18': request.POST.get('check_10_18'),
            'check_10_23': request.POST.get('check_10_23'),
            'check_10_03': request.POST.get('check_10_03'),
            'check_10_06': request.POST.get('check_10_06'),
            'check_11_14': request.POST.get('check_11_14'),
            'check_11_18': request.POST.get('check_11_18'),
            'check_11_23': request.POST.get('check_11_23'),
            'check_11_03': request.POST.get('check_11_03'),
            'check_11_06': request.POST.get('check_11_06'),
            'check_12_14': request.POST.get('check_12_14'),
            'check_12_18': request.POST.get('check_12_18'),
            'check_12_23': request.POST.get('check_12_23'),
            'check_12_03': request.POST.get('check_12_03'),
            'check_12_06': request.POST.get('check_12_06'),
            'check_13_14': request.POST.get('check_13_14'),
            'check_13_18': request.POST.get('check_13_18'),
            'check_13_23': request.POST.get('check_13_23'),
            'check_13_03': request.POST.get('check_13_03'),
            'check_13_06': request.POST.get('check_13_06'),
            'check_14_14': request.POST.get('check_14_14'),
            'check_14_18': request.POST.get('check_14_18'),
            'check_14_23': request.POST.get('check_14_23'),
            'check_14_03': request.POST.get('check_14_03'),
            'check_14_06': request.POST.get('check_14_06'),
            'check_15_14': request.POST.get('check_15_14'),
            'check_15_18': request.POST.get('check_15_18'),
            'check_15_23': request.POST.get('check_15_23'),
            'check_15_03': request.POST.get('check_15_03'),
            'check_15_06': request.POST.get('check_15_06'),
            'check_16_14': request.POST.get('check_16_14'),
            'check_16_18': request.POST.get('check_16_18'),
            'check_16_23': request.POST.get('check_16_23'),
            'check_16_03': request.POST.get('check_16_03'),
            'check_16_06': request.POST.get('check_16_06'),
            'check_17_14': request.POST.get('check_17_14'),
            'check_17_18': request.POST.get('check_17_18'),
            'check_17_23': request.POST.get('check_17_23'),
            'check_17_03': request.POST.get('check_17_03'),
            'check_17_06': request.POST.get('check_17_06'),
            'check_18_14': request.POST.get('check_18_14'),
            'check_18_18': request.POST.get('check_18_18'),
            'check_18_23': request.POST.get('check_18_23'),
            'check_18_03': request.POST.get('check_18_03'),
            'check_18_06': request.POST.get('check_18_06'),
            'check_19_14': request.POST.get('check_19_14'),
            'check_19_18': request.POST.get('check_19_18'),
            'check_19_23': request.POST.get('check_19_23'),
            'check_19_03': request.POST.get('check_19_03'),
            'check_19_06': request.POST.get('check_19_06'),
            'check_20_14': request.POST.get('check_20_14'),
            'check_20_18': request.POST.get('check_20_18'),
            'check_20_23': request.POST.get('check_20_23'),
            'check_20_03': request.POST.get('check_20_03'),
            'check_20_06': request.POST.get('check_20_06'),
            'check_21_14': request.POST.get('check_21_14'),
            'check_21_18': request.POST.get('check_21_18'),
            'check_21_23': request.POST.get('check_21_23'),
            'check_21_03': request.POST.get('check_21_03'),
            'check_21_06': request.POST.get('check_21_06'),
            'check_22_14': request.POST.get('check_22_14'),
            'check_22_18': request.POST.get('check_22_18'),
            'check_22_23': request.POST.get('check_22_23'),
            'check_22_03': request.POST.get('check_22_03'),
            'check_22_06': request.POST.get('check_22_06'),
            'check_23_14': request.POST.get('check_23_14'),
            'check_23_18': request.POST.get('check_23_18'),
            'check_23_23': request.POST.get('check_23_23'),
            'check_23_03': request.POST.get('check_23_03'),
            'check_23_06': request.POST.get('check_23_06'),
            'check_24_14': request.POST.get('check_24_14'),
            'check_24_18': request.POST.get('check_24_18'),
            'check_24_23': request.POST.get('check_24_23'),
            'check_24_03': request.POST.get('check_24_03'),
            'check_24_06': request.POST.get('check_24_06'),
            # Συλλογή δεδομένων για τον πίνακα ελέγχου γραμμών ΕΨΑΔ
            'checks': {
                'check_1_14': request.POST.get('check_1_14'),
                'check_1_18': request.POST.get('check_1_18'),
                'check_1_23': request.POST.get('check_1_23'),
                'check_1_03': request.POST.get('check_1_03'),
                'check_1_06': request.POST.get('check_1_06'),
                'check_2_14': request.POST.get('check_2_14'),
                'check_2_18': request.POST.get('check_2_18'),
                'check_2_23': request.POST.get('check_2_23'),
                'check_2_03': request.POST.get('check_2_03'),
                'check_2_06': request.POST.get('check_2_06'),
                'check_3_14': request.POST.get('check_3_14'),
                'check_3_18': request.POST.get('check_3_18'),
                'check_3_23': request.POST.get('check_3_23'),
                'check_3_03': request.POST.get('check_3_03'),
                'check_3_06': request.POST.get('check_3_06'),
                'check_4_14': request.POST.get('check_4_14'),
                'check_4_18': request.POST.get('check_4_18'),
                'check_4_23': request.POST.get('check_4_23'),
                'check_4_03': request.POST.get('check_4_03'),
                'check_4_06': request.POST.get('check_4_06'),
                'check_5_14': request.POST.get('check_5_14'),
                'check_5_18': request.POST.get('check_5_18'),
                'check_5_23': request.POST.get('check_5_23'),
                'check_5_03': request.POST.get('check_5_03'),
                'check_5_06': request.POST.get('check_5_06'),
                'check_6_14': request.POST.get('check_6_14'),
                'check_6_18': request.POST.get('check_6_18'),
                'check_6_23': request.POST.get('check_6_23'),
                'check_6_03': request.POST.get('check_6_03'),
                'check_6_06': request.POST.get('check_6_06'),
                'check_7_14': request.POST.get('check_7_14'),
                'check_7_18': request.POST.get('check_7_18'),
                'check_7_23': request.POST.get('check_7_23'),
                'check_7_03': request.POST.get('check_7_03'),
                'check_7_06': request.POST.get('check_7_06'),
                'check_8_14': request.POST.get('check_8_14'),
                'check_8_18': request.POST.get('check_8_18'),
                'check_8_23': request.POST.get('check_8_23'),
                'check_8_03': request.POST.get('check_8_03'),
                'check_8_06': request.POST.get('check_8_06'),
                'check_9_14': request.POST.get('check_9_14'),
                'check_9_18': request.POST.get('check_9_18'),
                'check_9_23': request.POST.get('check_9_23'),
                'check_9_03': request.POST.get('check_9_03'),
                'check_9_06': request.POST.get('check_9_06'),
                'check_10_14': request.POST.get('check_10_14'),
                'check_10_18': request.POST.get('check_10_18'),
                'check_10_23': request.POST.get('check_10_23'),
                'check_10_03': request.POST.get('check_10_03'),
                'check_10_06': request.POST.get('check_10_06'),
                'check_11_14': request.POST.get('check_11_14'),
                'check_11_18': request.POST.get('check_11_18'),
                'check_11_23': request.POST.get('check_11_23'),
                'check_11_03': request.POST.get('check_11_03'),
                'check_11_06': request.POST.get('check_11_06'),
                'check_12_14': request.POST.get('check_12_14'),
                'check_12_18': request.POST.get('check_12_18'),
                'check_12_23': request.POST.get('check_12_23'),
                'check_12_03': request.POST.get('check_12_03'),
                'check_12_06': request.POST.get('check_12_06'),
                'check_13_14': request.POST.get('check_13_14'),
                'check_13_18': request.POST.get('check_13_18'),
                'check_13_23': request.POST.get('check_13_23'),
                'check_13_03': request.POST.get('check_13_03'),
                'check_13_06': request.POST.get('check_13_06'),
                'check_14_14': request.POST.get('check_14_14'),
                'check_14_18': request.POST.get('check_14_18'),
                'check_14_23': request.POST.get('check_14_23'),
                'check_14_03': request.POST.get('check_14_03'),
                'check_14_06': request.POST.get('check_14_06'),
                'check_15_14': request.POST.get('check_15_14'),
                'check_15_18': request.POST.get('check_15_18'),
                'check_15_23': request.POST.get('check_15_23'),
                'check_15_03': request.POST.get('check_15_03'),
                'check_15_06': request.POST.get('check_15_06'),
                'check_16_14': request.POST.get('check_16_14'),
                'check_16_18': request.POST.get('check_16_18'),
                'check_16_23': request.POST.get('check_16_23'),
                'check_16_03': request.POST.get('check_16_03'),
                'check_16_06': request.POST.get('check_16_06'),
                'check_17_14': request.POST.get('check_17_14'),
                'check_17_18': request.POST.get('check_17_18'),
                'check_17_23': request.POST.get('check_17_23'),
                'check_17_03': request.POST.get('check_17_03'),
                'check_17_06': request.POST.get('check_17_06'),
                'check_18_14': request.POST.get('check_18_14'),
                'check_18_18': request.POST.get('check_18_18'),
                'check_18_23': request.POST.get('check_18_23'),
                'check_18_03': request.POST.get('check_18_03'),
                'check_18_06': request.POST.get('check_18_06'),
                'check_19_14': request.POST.get('check_19_14'),
                'check_19_18': request.POST.get('check_19_18'),
                'check_19_23': request.POST.get('check_19_23'),
                'check_19_03': request.POST.get('check_19_03'),
                'check_19_06': request.POST.get('check_19_06'),
                'check_20_14': request.POST.get('check_20_14'),
                'check_20_18': request.POST.get('check_20_18'),
                'check_20_23': request.POST.get('check_20_23'),
                'check_20_03': request.POST.get('check_20_03'),
                'check_20_06': request.POST.get('check_20_06'),
                'check_21_14': request.POST.get('check_21_14'),
                'check_21_18': request.POST.get('check_21_18'),
                'check_21_23': request.POST.get('check_21_23'),
                'check_21_03': request.POST.get('check_21_03'),
                'check_21_06': request.POST.get('check_21_06'),
                'check_22_14': request.POST.get('check_22_14'),
                'check_22_18': request.POST.get('check_22_18'),
                'check_22_23': request.POST.get('check_22_23'),
                'check_22_03': request.POST.get('check_22_03'),
                'check_22_06': request.POST.get('check_22_06'),
                'check_23_14': request.POST.get('check_23_14'),
                'check_23_18': request.POST.get('check_23_18'),
                'check_23_23': request.POST.get('check_23_23'),
                'check_23_03': request.POST.get('check_23_03'),
                'check_23_06': request.POST.get('check_23_06'),
                'check_24_14': request.POST.get('check_24_14'),
                'check_24_18': request.POST.get('check_24_18'),
                'check_24_23': request.POST.get('check_24_23'),
                'check_24_03': request.POST.get('check_24_03'),
                'check_24_06': request.POST.get('check_24_06'),
            }
        }

        # Δημιουργία του HTML από το template
        html_string = render_to_string('print_anafora_opliti.html', context)

        # Αποθήκευση του HTML σε προσωρινό αρχείο
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_html_file:
            temp_html_file.write(html_string.encode('utf-8'))
            temp_html_file_path = temp_html_file.name

        # Ανίχνευση του λειτουργικού συστήματος και διαμόρφωση του pdfkit
        if platform.system() == 'Windows':
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf.exe')
        elif platform.system() == 'Darwin':  # Darwin είναι το όνομα του πυρήνα του macOS
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf')
        else:
            raise Exception("Unsupported OS")

        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Δημιουργία του PDF από το προσωρινό αρχείο με επιπλέον options
        pdf = pdfkit.from_file(temp_html_file_path, False, configuration=pdfkit_config, options={
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',  # Αυτό επιτρέπει την πρόσβαση σε τοπικά αρχεία
            'orientation': 'Portrait'  # Καθορίζει την οριζόντια εκτύπωση
        })

        # Αποθήκευση του PDF στο μοντέλο
        service_report = OplitiServiceReport()
        service_report.pdf.save('Αναφορά_Οπλίτη_{}.pdf'.format(datetime.now().strftime('%d-%m-%Y')), ContentFile(pdf))

        # Ανακατεύθυνση ή εμφάνιση της σελίδας με το PDF
        return HttpResponse(pdf, content_type='application/pdf')

    # Εμφάνιση της φόρμας για συμπλήρωση
    return render(request, 'anafora_ipiresia_opliti.html')

def vtc_view(request):
    return render(request, 'vtc.html')

def pyrseia_view(request):
    return render(request, 'pyrseia.html')

def dides_view(request):
    return render(request, 'dides.html')

def katastaseis_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Φιλτράρισμα με βάση το εύρος ημερομηνιών
    if start_date and end_date:
        reports = ServiceReportSummary.objects.filter(report_date__range=[start_date, end_date])
    else:
        reports = ServiceReportSummary.objects.all()

    # Υπολογισμός των συνολικών συνόλων
    total_sda = reports.aggregate(Sum('total_sda'))['total_sda__sum'] or 0
    total_aifs = reports.aggregate(Sum('total_aifs'))['total_aifs__sum'] or 0
    total_cronos = reports.aggregate(Sum('total_cronos'))['total_cronos__sum'] or 0
    total_general = reports.aggregate(Sum('total_general'))['total_general__sum'] or 0

    context = {
        'total_sda': total_sda,
        'total_aifs': total_aifs,
        'total_cronos': total_cronos,
        'total_general': total_general
    }
    return render(request, 'katastaseis.html', context)


def posta_view(request):
    if request.method == 'POST':
        # Παίρνουμε την ημερομηνία από τη φόρμα
        service_date = request.POST.get('service_date')

        # Φορμάρουμε την ημερομηνία και ελέγχουμε αν είναι καθημερινή ή Σαββατοκύριακο
        if service_date:
            formatted_date = datetime.strptime(service_date, '%Y-%m-%d').strftime('%d %B %Y')
            date_object = datetime.strptime(service_date, '%Y-%m-%d')
            # Ελέγχει αν είναι Σαββατοκύριακο (5 = Σάββατο, 6 = Κυριακή)
            if date_object.weekday() >= 5:
                day_type = 'Σαββατοκύριακο'
            else:
                day_type = 'Καθημερινή'
        else:
            formatted_date = 'Χωρίς Ημερομηνία'
            day_type = 'Άγνωστο'

        context = {
            'soldiers': Soldier.objects.all(),
            'service_date': formatted_date,  # Ημερομηνία για τον τίτλο
            'day_type': day_type  # Κατηγοριοποίηση αν είναι καθημερινή ή ΣΚ
        }
        return render(request, 'posta.html', context)

    return render(request, 'posta.html', {'soldiers': Soldier.objects.all(), 'service_date': 'Χωρίς Ημερομηνία', 'day_type': 'Άγνωστο'})

def passwords_view(request):
    # Φόρτωση δεδομένων ανά κατηγορία από τη βάση δεδομένων
    computers = AxypCodesCategory.objects.filter(item_type='computers')
    pyrseia = AxypCodesCategory.objects.filter(item_type='pyrseia')
    applications = AxypCodesCategory.objects.filter(item_type='applications')
    staff = AxypCodesCategory.objects.filter(item_type='staff')
    useful_phones = AxypCodesCategory.objects.filter(item_type='useful_phones')
    phone_codes = AxypCodesCategory.objects.filter(item_type='phone_codes')

    # Σύνδεση των δεδομένων με το template
    context = {
        'computers': computers,
        'pyrseia': pyrseia,
        'applications': applications,
        'staff': staff,
        'useful_phones': useful_phones,
        'phone_codes': phone_codes,
    }

    # Απόδοση του template με τα δεδομένα
    return render(request, 'passwords.html', context)

from django.shortcuts import render
from myapp.models import HARPDirectory, VOSIPTelephoneDirectory, KlistoTilefoniko

def katalogoi_view(request):
    harp_entries = HARPDirectory.objects.all()
    vosip_entries = VOSIPTelephoneDirectory.objects.all()
    klisto_entries = KlistoTilefoniko.objects.all()
    
    context = {
        'harp_entries': harp_entries,
        'vosip_entries': vosip_entries,
        'klisto_entries': klisto_entries,
    }
    
    return render(request, 'katalogoi.html', context)

def print_posta_view(request):
    if request.method == 'POST':
        soldiers_data = []
        services_data = []
        exodouxoi_data = []
        adeies_data = []

        # Παίρνουμε την ημερομηνία από το POST
        service_date = request.POST.get('service_date')

        # Φορμάρουμε την ημερομηνία και ελέγχουμε αν είναι καθημερινή ή Σαββατοκύριακο
        if service_date:
            formatted_date = datetime.strptime(service_date, '%Y-%m-%d').strftime('%d %B %Y')
            date_object = datetime.strptime(service_date, '%Y-%m-%d')
            # Ελέγχει αν είναι Σαββατοκύριακο (5 = Σάββατο, 6 = Κυριακή)
            if date_object.weekday() >= 5:
                day_type = 'Σαββατοκύριακο'
            else:
                day_type = 'Καθημερινή'
        else:
            formatted_date = 'Χωρίς Ημερομηνία'
            day_type = 'Άγνωστο'

        # Συλλογή δεδομένων από τη φόρμα
        soldiers = zip(
            request.POST.getlist('soldier_name[]'),
            request.POST.getlist('posto[]'),
            request.POST.getlist('ypiresiako[]'),
            request.POST.getlist('dianyktereysi[]'),
            request.POST.getlist('metavoles[]'),
            request.POST.getlist('apo[]'),
            request.POST.getlist('eos[]'),
            request.POST.getlist('kathariotites[]')
        )

        for soldier in soldiers:
            soldiers_data.append({
                'soldier_name': soldier[0],
                'posto': soldier[1],
                'ypiresiako': soldier[2],
                'dianyktereysi': soldier[3],
                'metavoles': soldier[4],
                'apo': soldier[5],
                'eos': soldier[6],
                'kathariotites': soldier[7],
            })

        # Υπολογισμοί για τα γενικά στοιχεία λόχου
        dynamis_lochou = len(soldiers_data)
        apousies = sum(1 for s in soldiers_data if s['metavoles'])
        parousies = dynamis_lochou - apousies

        # Υπολογισμοί για τα ειδικά στοιχεία λόχου
        timitikes = sum(1 for s in soldiers_data if s['metavoles'] == "Τιμητική Άδεια")
        loipes_adeies = sum(1 for s in soldiers_data if s['metavoles'] in ["Κανονική Άδεια", "Αγροτική Άδεια", "Αιμοδοτική Άδεια", "Αναρρωτική Άδεια", "Φοιτητική Άδεια", "Άδεια Ορκομωσίας"])
        ypiresiaka = sum(1 for s in soldiers_data if s['metavoles'] == "Υπηρεσιακό")
        apospathseis = sum(1 for s in soldiers_data if s['metavoles'] == "Απόσπαση")
        ey = sum(1 for s in soldiers_data if s['metavoles'] == "ΕΥ")
        synolo = timitikes + loipes_adeies + ypiresiaka + apospathseis + ey

        # Υπηρεσίες σήμερα και εφεδρικοί
        for soldier in soldiers_data:
            if soldier['metavoles'] in ["ΤΗΠ", "ΤΦ", "Θ", "ΟΥ", "ΕΝ", "Εφεδρικός"]:
                services_data.append({
                    'soldier_name': soldier['soldier_name'],
                    'metavoli': soldier['metavoles'],
                })

        # Κατάσταση εξοδούχων
        for soldier in soldiers_data:
            if soldier['ypiresiako'] and soldier['dianyktereysi']:
                exodouxoi_data.append({
                    'soldier_name': soldier['soldier_name'],
                    'ypiresiako': soldier['ypiresiako'],
                    'dianyktereysi': soldier['dianyktereysi'],
                })

        # Κατάσταση αδειούχων
        for soldier in soldiers_data:
            if soldier['metavoles'] in ["Τιμητική Άδεια", "Κανονική Άδεια", "Αγροτική Άδεια", "Αιμοδοτική Άδεια", "Αναρρωτική Άδεια", "Φοιτητική Άδεια"]:
                adeies_data.append({
                    'soldier_name': soldier['soldier_name'],
                    'eidos_adeias': soldier['metavoles'],
                    'apo': soldier['apo'],
                    'eos': soldier['eos'],
                })

        # Δημιουργία του context για το template
        context = {
            'soldiers': soldiers_data,
            'dynamis_lochou': dynamis_lochou,
            'apousies': apousies,
            'parousies': parousies,
            'timitikes': timitikes,
            'loipes_adeies': loipes_adeies,
            'ypiresiaka': ypiresiaka,
            'apospathseis': apospathseis,
            'ey': ey,
            'synolo': synolo,
            'services': services_data,
            'exodouxoi': exodouxoi_data,
            'adeies': adeies_data,
            'service_date': formatted_date,  # Περνάμε την ημερομηνία στο context
            'day_type': day_type  # Καθημερινή ή Σαββατοκύριακο
        }

        # Δημιουργία του HTML από το template
        html_string = render_to_string('Print_posta.html', context)

        # Αποθήκευση του HTML σε προσωρινό αρχείο
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_html_file:
            temp_html_file.write(html_string.encode('utf-8'))
            temp_html_file_path = temp_html_file.name

        # Ανίχνευση του λειτουργικού συστήματος και διαμόρφωση του pdfkit
        if platform.system() == 'Windows':
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf.exe')
        elif platform.system() == 'Darwin':  # macOS
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf')
        else:
            raise Exception("Unsupported OS")

        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Δημιουργία του PDF από το προσωρινό αρχείο
        pdf = pdfkit.from_file(temp_html_file_path, False, configuration=pdfkit_config, options={
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',
            'orientation': 'Landscape'  # Καθορίζει την οριζόντια εκτύπωση
        })

        # Επιστροφή του PDF ως απάντηση HTTP
        return HttpResponse(pdf, content_type='application/pdf')

    return render(request, 'posta.html')

def test_exodocharta_view(request):
    if request.method == 'POST':
        # Παίρνουμε τους επιλεγμένους στρατιώτες
        selected_soldiers_ids = request.POST.getlist('selected_soldiers')
        soldiers = Soldier.objects.filter(id__in=selected_soldiers_ids)
        
        # Παίρνουμε τον επιλεγμένο αξιωματικό και ιδιότητα
        officer = OfficerServiceReport.objects.get(id=request.POST.get('officer'))
        role = request.POST.get('role')
        
        # Παίρνουμε την ημερομηνία και την ώρα εξόδου
        exit_date = request.POST.get('exit_date')  # Αρχικά παίρνουμε την τιμή ως string
        exit_time = request.POST.get('exit_time')

        # Μετατρέπουμε την ημερομηνία σε format dd/mm/yyyy
        formatted_exit_date = datetime.strptime(exit_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        context = {
            'soldiers': soldiers,
            'officer': officer,
            'role': role,
            'exit_date': formatted_exit_date,  # Χρησιμοποιούμε την μορφοποιημένη ημερομηνία
            'exit_time': exit_time,
        }
        
        return render(request, 'test.html', context)

    # Σε περίπτωση GET, επιστρέφουμε το exodoxarta.html
    soldiers = Soldier.objects.all().order_by('eponymo')
    officers = OfficerServiceReport.objects.all().order_by('last_name')
    return render(request, 'exodoxarta.html', {'soldiers': soldiers, 'officers': officers})

def exodoxarta_view(request):
    if request.method == 'POST':
        # Λήψη των στρατιωτών και του αξιωματικού που επιλέχθηκαν
        selected_soldiers_ids = request.POST.getlist('selected_soldiers')
        selected_soldiers = Soldier.objects.filter(id__in=selected_soldiers_ids)
        selected_officer_id = request.POST.get('officer')
        selected_officer = OfficerServiceReport.objects.get(id=selected_officer_id)
        selected_role = request.POST.get('role')  # Λήψη της επιλεγμένης ιδιότητας
        exit_date = request.POST.get('exit_date')  # Λήψη της ημερομηνίας
        exit_time = request.POST.get('exit_time')  # Λήψη της ώρας εξόδου

        # Προσθήκη των επιλεγμένων στο context για χρήση στο exodocharta_template
        context = {
            'selected_soldiers': selected_soldiers,
            'selected_officer': selected_officer,
            'selected_role': selected_role,
            'exit_date': exit_date,  # Προσθήκη της ημερομηνίας
            'exit_time': exit_time,  # Προσθήκη της ώρας εξόδου
        }

        # Render το template για να εμφανιστούν τα εξοδόχαρτα
        return render(request, 'test.html', context)

    # Φόρτωση στρατιωτών και αξιωματικών
    soldiers = Soldier.objects.all().order_by('eponymo')  # Ταξινόμηση κατά επώνυμο
    officers = OfficerServiceReport.objects.all()

    return render(request, 'exodoxarta.html', {'soldiers': soldiers, 'officers': officers})

def yphresiaka_view(request):
    if request.method == 'POST':
        # Παίρνουμε τους επιλεγμένους στρατιώτες
        selected_soldiers_ids = request.POST.getlist('selected_soldiers')
        soldiers = Soldier.objects.filter(id__in=selected_soldiers_ids)
        
        # Σταθερή ιδιότητα "Δ Ι Ο Ι Κ Η Τ Η Σ"
        role = "Δ Ι Ο Ι Κ Η Τ Η Σ"
        
        # Παίρνουμε την ημερομηνία εξόδου
        exit_date = request.POST.get('exit_date')
        formatted_exit_date = datetime.strptime(exit_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        # Υπολογισμός της αυτόματης ώρας εξόδου με βάση την ημερομηνία
        selected_date = datetime.strptime(exit_date, '%Y-%m-%d')
        day_of_week = selected_date.weekday()  # 0 = Δευτέρα, 6 = Κυριακή
        if day_of_week == 6:  # Κυριακή
            auto_exit_time = '10:00'
        elif day_of_week == 5:  # Σάββατο
            auto_exit_time = '12:00'
        else:  # Καθημερινές
            auto_exit_time = '14:30'
        
        # Παίρνουμε την ώρα που επιλέγεται για κάθε στρατιώτη
        soldiers_with_times = []
        for soldier in soldiers:
            selected_time = request.POST.get(f'time_{soldier.id}', None)  # Ώρα για κάθε στρατιώτη
            if selected_time:
                soldiers_with_times.append({
                    'soldier': soldier,
                    'selected_time': selected_time,  # Η επιλεγμένη ώρα για κάθε στρατιώτη
                    'auto_exit_time': auto_exit_time  # Αυτόματα υπολογισμένη ώρα εξόδου
                })

        # Προσθήκη των δεδομένων στο context
        context = {
            'soldiers_with_times': soldiers_with_times,
            'role': role,
            'exit_date': formatted_exit_date,
            'auto_exit_time': auto_exit_time  # Αυτόματα υπολογισμένη ώρα εξόδου για την αναφορά
        }

        # Render το template για εμφάνιση των υπηρεσιακών
        return render(request, 'test_yphresiaka.html', context)

    # Σε περίπτωση GET, επιστρέφουμε το yphresiaka.html
    soldiers = Soldier.objects.all().order_by('eponymo')
    time_choices = ['06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', 
                    '13:30', '14:00']

    return render(request, 'yphresiaka.html', {'soldiers': soldiers, 'time_choices': time_choices})

def test_yphresiaka_view(request):
    if request.method == 'POST':
        # Παίρνουμε τους επιλεγμένους στρατιώτες
        selected_soldiers_ids = request.POST.getlist('selected_soldiers')
        soldiers = Soldier.objects.filter(id__in=selected_soldiers_ids)
        
        # Σταθερή ιδιότητα "Δ Ι Ο Ι Κ Η Τ Η Σ"
        role = "Δ Ι Ο Ι Κ Η Τ Η Σ"
        
        # Παίρνουμε την ημερομηνία εξόδου
        exit_date = request.POST.get('exit_date')
        formatted_exit_date = datetime.strptime(exit_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        # Υπολογισμός της ώρας εξόδου με βάση την ημερομηνία
        selected_date = datetime.strptime(exit_date, '%Y-%m-%d')
        day_of_week = selected_date.weekday()  # 0 = Δευτέρα, 6 = Κυριακή
        if day_of_week == 6:  # Κυριακή
            auto_exit_time = '10:00'
        elif day_of_week == 5:  # Σάββατο
            auto_exit_time = '12:00'
        else:  # Καθημερινές
            auto_exit_time = '14:30'
        
        # Παίρνουμε την ώρα για κάθε στρατιώτη
        soldiers_with_times = []
        for soldier in soldiers:
            selected_time = request.POST.get(f'time_{soldier.id}', None)  # Ώρα που επιλέχθηκε για κάθε στρατιώτη
            if selected_time:
                soldiers_with_times.append({
                    'soldier': soldier,
                    'selected_time': selected_time,  # Ώρα που επιλέχθηκε για τον στρατιώτη
                    'auto_exit_time': auto_exit_time  # Αυτόματα υπολογισμένη ώρα εξόδου
                })

        # Προσθήκη δεδομένων στο context
        context = {
            'soldiers_with_times': soldiers_with_times,
            'role': role,
            'exit_date': formatted_exit_date,
            'auto_exit_time': auto_exit_time  # Αυτόματα υπολογισμένη ώρα εξόδου για την αναφορά
        }
        
        # Render το template για τα υπηρεσιακά
        return render(request, 'test_yphresiaka.html', context)

    # Σε περίπτωση GET, επιστρέφουμε το yphresiaka.html
    soldiers = Soldier.objects.all().order_by('eponymo')
    return render(request, 'yphresiaka.html', {'soldiers': soldiers})

from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Soldier

def adeioxarta_view(request):
    if request.method == 'POST':
        # Παίρνουμε τους επιλεγμένους στρατιώτες
        selected_soldiers_ids = request.POST.getlist('selected_soldiers')
        soldiers = Soldier.objects.filter(id__in=selected_soldiers_ids)
        
        # Παίρνουμε την σταθερή ιδιότητα "Δ Ι Ο Ι Κ Η Τ Η Σ"
        role = "Δ Ι Ο Ι Κ Η Τ Η Σ"
        
        # Παίρνουμε την ημερομηνία "Αρχομένης"
        start_date = request.POST.get('start_date')
        formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        
        # Παίρνουμε τη διάρκεια σε ημέρες
        duration = int(request.POST.get('duration'))

        # Υπολογισμός ημερομηνίας λήξης
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = start_date_obj + timedelta(days=duration)
        formatted_end_date = end_date_obj.strftime('%d/%m/%Y')

        # Παίρνουμε την ημερομηνία εκτύπωσης
        print_date = request.POST.get('print_date')
        formatted_print_date = datetime.strptime(print_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        # Παίρνουμε τον τύπο άδειας για κάθε στρατιώτη
        soldiers_with_leaves = []
        for soldier in soldiers:
            leave_type = request.POST.get(f'leave_type_{soldier.id}', None)  # Ο τύπος άδειας για κάθε στρατιώτη
            if leave_type:
                soldiers_with_leaves.append({
                    'soldier': soldier,
                    'leave_type': leave_type,  # Ο τύπος άδειας
                    'start_date': formatted_start_date,  # Ημερομηνία έναρξης
                    'end_date': formatted_end_date,  # Ημερομηνία λήξης
                    'print_date': formatted_print_date  # Ημερομηνία εκτύπωσης
                })

        # Προσθήκη δεδομένων στο context
        context = {
            'soldiers_with_leaves': soldiers_with_leaves,
            'role': role,
            'start_date': formatted_start_date,
            'end_date': formatted_end_date,
            'duration': duration,
            'print_date': formatted_print_date  # Προσθήκη της ημερομηνίας εκτύπωσης στο context
        }
        
        # Render το template για εμφάνιση των αδειοχάρτων
        return render(request, 'test_adeioxarta.html', context)

    # Σε περίπτωση GET, επιστρέφουμε το adeioxarta.html
    soldiers = Soldier.objects.all().order_by('eponymo')
    
    # Προσθήκη του εύρους της διάρκειας (1-18) στο context
    duration_range = range(1, 19)

    return render(request, 'adeioxarta.html', {'soldiers': soldiers, 'duration_range': duration_range})

def test_adeioxarta_view(request):
    if request.method == 'POST':
        # Παίρνουμε τους επιλεγμένους στρατιώτες
        selected_soldiers_ids = request.POST.getlist('selected_soldiers')
        soldiers = Soldier.objects.filter(id__in=selected_soldiers_ids)
        
        # Παίρνουμε την σταθερή ιδιότητα "Δ Ι Ο Ι Κ Η Τ Η Σ"
        role = "Δ Ι Ο Ι Κ Η Τ Η Σ"
        
        # Παίρνουμε την ημερομηνία "Αρχομένης"
        start_date = request.POST.get('start_date')
        formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        
        # Παίρνουμε τη διάρκεια σε ημέρες
        duration = int(request.POST.get('duration'))

        # Υπολογισμός ημερομηνίας λήξης
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = start_date_obj + timedelta(days=duration)
        formatted_end_date = end_date_obj.strftime('%d/%m/%Y')

        # Παίρνουμε τον τύπο άδειας για κάθε στρατιώτη
        soldiers_with_leaves = []
        for soldier in soldiers:
            leave_type = request.POST.get(f'leave_type_{soldier.id}', None)  # Ο τύπος άδειας για κάθε στρατιώτη
            if leave_type:
                soldiers_with_leaves.append({
                    'soldier': soldier,
                    'leave_type': leave_type,  # Ο τύπος άδειας
                    'start_date': formatted_start_date,  # Ημερομηνία έναρξης
                    'end_date': formatted_end_date  # Ημερομηνία λήξης
                })

        # Προσθήκη δεδομένων στο context
        context = {
            'soldiers_with_leaves': soldiers_with_leaves,
            'role': role,
            'start_date': formatted_start_date,
            'end_date': formatted_end_date,
            'duration': duration,
        }
        
        # Render το template για εμφάνιση των αδειοχάρτων
        return render(request, 'test_adeioxarta.html', context)

    # Σε περίπτωση GET, επιστρέφουμε το adeioxarta.html
    soldiers = Soldier.objects.all().order_by('eponymo')
    return render(request, 'adeioxarta.html', {'soldiers': soldiers})