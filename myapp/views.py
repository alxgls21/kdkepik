from django.shortcuts import render, redirect
from django.db.models import Sum
from django.template.loader import render_to_string
from .models import DidesCategory, HarpCategory, AdmeCategory, OfficerServiceReport, Soldier, AxypKepikServiceReport, OplitiServiceReport, ServiceReportSummary
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
import platform
from django.urls import reverse
from django.shortcuts import redirect
from .forms import SoldierForm, SummaryForm, SpecialDetailsForm, CurrentServiceForm, ExodouchoiForm, RegularLeaveForm, SpecialCaseForm, HonorLeaveForm


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


from django.shortcuts import render
from .models import Soldier
from .forms import SoldierForm, SummaryForm

def posta_view(request):
    if request.method == 'POST':
        # Παίρνουμε την ημερομηνία
        report_date = request.POST.get('report_date', datetime.now().strftime('%Y-%m-%d'))
        formatted_date = datetime.strptime(report_date, '%Y-%m-%d').strftime('%d/%m/%Y')

        # Συλλογή δεδομένων στρατιωτών από τη φόρμα
        total_force = int(request.POST.get('total_force', 0))
        soldiers_data = []
        for i in range(1, total_force + 1):
            soldier_form = SoldierForm({
                'post': request.POST.get(f'post_{i}', ''),
                'service': request.POST.get(f'service_{i}', ''),
                'night': request.POST.get(f'night_{i}', ''),
                'change': request.POST.get(f'change_{i}', ''),
                'duration': request.POST.get(f'duration_{i}', ''),
                'from_date': request.POST.get(f'from_{i}', None),
                'to_date': request.POST.get(f'to_{i}', None),
                'cleaning': request.POST.get(f'cleaning_{i}', ''),
            })

            if soldier_form.is_valid():
                cleaned_data = soldier_form.cleaned_data
                from_date = cleaned_data.get('from_date')
                to_date = cleaned_data.get('to_date')

                # Προσθήκη δεδομένων στρατιώτη στη λίστα
                soldiers_data.append({
                    'soldier_form': cleaned_data,
                    'from_date': from_date.strftime('%d/%m/%Y') if from_date else '',
                    'to_date': to_date.strftime('%d/%m/%Y') if to_date else '',
                })

        # Συγκεντρωτικά Στοιχεία
        summary_form = SummaryForm({
            'absences': request.POST.get('absences', ''),
            'present': request.POST.get('present', ''),
        })
        summary_data = summary_form.cleaned_data if summary_form.is_valid() else {}

        # Ειδικά Στοιχεία
        special_data = {
            'honor_leaves': request.POST.get('honor_leaves', '0'),
            'regular_leaves': request.POST.get('regular_leaves', '0'),
            'service_leaves': request.POST.get('service_leaves', '0'),
            'ey_leaves': request.POST.get('ey_leaves', '0'),
            'detachments': request.POST.get('detachments', '0'),
            'total_special': request.POST.get('total_special', '0')
        }

        # Δημιουργία context για το template
        context = {
            'date': formatted_date,
            'soldiers_data': soldiers_data,
            'summary_data': summary_data,
            'special_data': special_data,
            'current_service': [],  # Προσθέστε δεδομένα από τη φόρμα
            'exodouchoi': [],  # Προσθέστε δεδομένα από τη φόρμα
            'regular_leaves': [],  # Προσθέστε δεδομένα από τη φόρμα
            'special_cases': [],  # Προσθέστε δεδομένα από τη φόρμα
            'honor_leaves': []  # Προσθέστε δεδομένα από τη φόρμα
        }

        # Δημιουργία του HTML από το template
        html_string = render_to_string('print_posta.html', context)

        # Αποθήκευση του HTML σε προσωρινό αρχείο
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_html_file:
            temp_html_file.write(html_string.encode('utf-8'))
            temp_html_file_path = temp_html_file.name

        # Ανίχνευση του λειτουργικού συστήματος και διαμόρφωση του pdfkit
        if platform.system() == 'Windows':
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf.exe')
        elif platform.system() == 'Darwin':
            wkhtmltopdf_path = os.path.join('myapp', 'bin', 'wkhtmltopdf')
        else:
            raise Exception("Unsupported OS")

        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Δημιουργία του PDF από το προσωρινό αρχείο με επιπλέον options
        pdf = pdfkit.from_file(temp_html_file_path, False, configuration=pdfkit_config, options={
            'no-stop-slow-scripts': '',
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',
            'orientation': 'Landscape'
        })

        # Αποθήκευση του PDF
        service_report = AxypKepikServiceReport()
        service_report.pdf.save(f'Posta_Report_{datetime.now().strftime("%d-%m-%Y")}.pdf', ContentFile(pdf))

        # Επιστροφή του PDF στον χρήστη
        return HttpResponse(pdf, content_type='application/pdf')

    # Εμφάνιση της φόρμας σε GET request
    soldiers = Soldier.objects.all().order_by('last_name')
    soldiers_data = [{'rank': soldier.rank, 'last_name': soldier.last_name, 'first_name': soldier.first_name} for soldier in soldiers]

    context = {
        'soldiers': soldiers_data
    }

    return render(request, 'posta.html', context)