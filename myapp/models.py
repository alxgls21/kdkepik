from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile
import os
from datetime import datetime

class DidesCategory(models.Model):
    UNCLASSIFIED_NETWORK = 'unclassified'
    CLASSIFIED_NETWORK = 'classified'
    CATEGORY_CHOICES = [
        (UNCLASSIFIED_NETWORK, _('Αδιαβάθμητο Δίκτυο DCE')),
        (CLASSIFIED_NETWORK, _('Διαβαθμισμένο Δίκτυο DTE')),
    ]
    
    MONITORING = 'monitoring'
    KEPIK_APPS = 'kepik_apps'
    USEFUL_LINKS = 'useful_links'
    PYRSEIA = 'pyrseia'
    VOSIP = 'vosip'
    APPLICATION_CHOICES = [
        (MONITORING, _('Monitoring')),
        (KEPIK_APPS, _('Εφαρμογές ΚΕΠΙΚ')),
        (USEFUL_LINKS, _('Χρήσιμοι Σύνδεσμοι')),
        (PYRSEIA, _('ΠΥΡΣΕΙΑ')),
        (VOSIP, _('VOSIP')),
    ]
    
    category = models.CharField(_('Κατηγορία'), max_length=20, choices=CATEGORY_CHOICES)
    application = models.CharField(_('Εφαρμογή'), max_length=20, choices=APPLICATION_CHOICES)
    name = models.CharField(_('Όνομα'), max_length=100)
    ip_address = models.URLField(_('Διεύθυνση IP'), blank=True, null=True)  # Χρήση URLField για πλήρη URLs
    supervisory_tool = models.CharField(_('Εποπτικό Μέσο'), max_length=100, blank=True)

    def __str__(self):
        return f'{self.name} ({self.get_category_display()}, {self.get_application_display()})'

    class Meta:
        verbose_name = _('Πεδία Ελέγχου | ΔΙΔΕΣ')
        verbose_name_plural = _('Πεδία Ελέγχου | ΔΙΔΕΣ')

class HarpCategory(models.Model):
    name = models.CharField(_('Όνομα'), max_length=100)
    ip_address = models.URLField(_('Διεύθυνση IP'), blank=True, null=True)  # Χρήση URLField για πλήρη URLs
    supervisory_tool = models.CharField(_('Εποπτικό Μέσο'), max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Πεδία Ελέγχου | HARP')
        verbose_name_plural = _('Πεδία Ελέγχου | HARP')

class AdmeCategory(models.Model):
    name = models.CharField(_('Όνομα'), max_length=100)
    ip_address = models.URLField(_('Διεύθυνση IP'), blank=True, null=True)  # Χρήση URLField για πλήρη URLs
    supervisory_tool = models.CharField(_('Εποπτικό Μέσο'), max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Πεδία Ελέγχου | ΑΔΜΕ')
        verbose_name_plural = _('Πεδία Ελέγχου | ΑΔΜΕ')

class OfficerServiceReport(models.Model):
    rank = models.CharField(_('Βαθμός'), max_length=50)
    last_name = models.CharField(_('Επώνυμο'), max_length=100)
    first_name = models.CharField(_('Όνομα'), max_length=100)
    phone_number = models.CharField(_('Τηλ Επικοινωνίας'), max_length=15)

    class Meta:
        verbose_name = _('Οργάνωση | Αξιωματικός Υπηρεσίας ΚΕΠΙΚ')
        verbose_name_plural = _('Οργάνωση | Αξιωματικοί Υπηρεσίας ΚΕΠΙΚ')

    def __str__(self):
        return f'{self.rank} {self.last_name} {self.first_name}'
    
class Soldier(models.Model):
    # Επιλογές για dropdowns
    VATHMOS_CHOICES = [
        ('ΣΤΡ(ΔΒ)', 'ΣΤΡ(ΔΒ)'),
        ('ΣΤΡ(ΠΖ)', 'ΣΤΡ(ΠΖ)'),
        ('ΣΤΡ(ΠΒ)', 'ΣΤΡ(ΠΒ)'),
        ('ΣΤΡ(ΤΘ)', 'ΣΤΡ(ΤΘ)'),
    ]

    GRAMMATIKES_GNOSEIS_CHOICES = [
        ('Απόφοιτος Λυκείου', 'Απόφοιτος Λυκείου'),
        ('Απόφοιτος ΑΕΙ', 'Απόφοιτος ΑΕΙ'),
        ('Απόφοιτος ΤΕΙ', 'Απόφοιτος ΤΕΙ'),
        ('Ενεργός ΑΕΙ', 'Ενεργός ΑΕΙ'),
        ('Ενεργός ΤΕΙ', 'Ενεργός ΤΕΙ'),
        ('Απόφοιτος ΙΕΚ', 'Απόφοιτος ΙΕΚ'),
        ('Ενεργός ΙΕΚ', 'Ενεργός ΙΕΚ'),
    ]

    SOMATIKI_IKANOTITA_CHOICES = [
        ('Ι1', 'Ι1'),
        ('Ι2', 'Ι2'),
        ('Ι3', 'Ι3'),
        ('Ι3 Άοπλο', 'Ι3 Άοπλο'),
        ('Ι4', 'Ι4'),
    ]
    
    POSTO_CHOICES = [
        ('HARP', 'HARP'),
        ('Helpdesk', 'Helpdesk'),
        ('Διαχείριση Δικτύων / Κυκλωμάτων', 'Διαχείριση Δικτύων / Κυκλωμάτων'),
        ('Τηλέτυπα', 'Τηλέτυπα'),
        ('Τηλεφωνικό', 'Τηλεφωνικό'),
        ('Τμήμα ΟΤΕ', 'Τμήμα ΟΤΕ'),
        ('ΥΕΣΑ', 'ΥΕΣΑ'),
    ]

    # Προσωπικά Στοιχεία
    eponymo = models.CharField(max_length=100, verbose_name="ΕΠΩΝΥΜΟ", null=True, blank=True)
    onoma = models.CharField(max_length=100, verbose_name="ΟΝΟΜΑ", null=True, blank=True)
    etos_genniseos = models.IntegerField(verbose_name="ΕΤΟΣ ΓΕΝΝΗΣΕΩΣ", null=True, blank=True)
    topos_genniseos = models.CharField(max_length=100, verbose_name="ΤΟΠΟΣ ΓΕΝΝΗΣΕΩΣ", null=True, blank=True)
    onoma_patros = models.CharField(max_length=100, verbose_name="ΟΝΟΜΑ ΠΑΤΕΡΑ", null=True, blank=True)
    epaggelma_patros = models.CharField(max_length=100, verbose_name="ΕΠΑΓΓΕΛΜΑ ΠΑΤΕΡΑ", null=True, blank=True)
    onoma_mitros = models.CharField(max_length=100, verbose_name="ΟΝΟΜΑ ΜΗΤΕΡΑΣ", null=True, blank=True)
    epaggelma_mitros = models.CharField(max_length=100, verbose_name="ΕΠΑΓΓΕΛΜΑ ΜΗΤΕΡΑΣ", null=True, blank=True)
    tilefono_kinito = models.CharField(max_length=10, verbose_name="ΤΗΛ. ΚΙΝΗΤΟ", null=True, blank=True)
    tilefono_stathero = models.CharField(max_length=10, verbose_name="ΤΗΛ. ΣΤΑΘΕΡΟ", null=True, blank=True)
    tilefono_oikeiou = models.CharField(max_length=10, verbose_name="ΤΗΛΕΦΩΝΟ ΟΙΚΕΙΟΥ", null=True, blank=True)
    oikeiou_sxesi = models.CharField(max_length=100, verbose_name="ΣΧΕΣΗ ΜΕ ΤΟΝ ΟΙΚΕΙΟ", null=True, blank=True)
    topos_katagogis = models.CharField(max_length=255, verbose_name="ΤΟΠΟΣ ΚΑΤΑΓΩΓΗΣ", null=True, blank=True)
    topos_diamonis = models.CharField(max_length=255, verbose_name="ΤΟΠΟΣ ΔΙΑΜΟΝΗΣ", null=True, blank=True)
    periochi = models.CharField(max_length=100, verbose_name="ΠΕΡΙΟΧΗ", null=True, blank=True)
    odos_arithmos = models.CharField(max_length=255, verbose_name="ΟΔΟΣ ΚΑΙ ΑΡΙΘΜΟΣ", null=True, blank=True)
    oikogeneiaki_katastasi = models.CharField(max_length=100, verbose_name="ΟΙΚΟΓ. ΚΑΤΑΣΤΑΣΗ", null=True, blank=True)
    arithmos_adelfon = models.CharField(max_length=100, verbose_name="ΑΡΙΘΜΟΣ ΑΔΕΛΦΩΝ – ΦΥΛΛΟ", null=True, blank=True)
    oikonomiki_katastasi = models.CharField(max_length=100, verbose_name="ΟΙΚΟΝ. ΚΑΤΑΣΤΑΣΗ", null=True, blank=True)
    provlimata_pou_apasxoloun = models.TextField(blank=True, null=True, verbose_name="ΠΡΟΒΛΗΜΑΤΑ ΠΟΥ ΑΠΑΣΧΟΛΟΥΝ")

    # Εκπαίδευση - Επάγγελμα
    epaggelma_politis = models.CharField(max_length=100, verbose_name="ΕΠΑΓΓΕΛΜΑ ΩΣ ΠΟΛΙΤΗΣ", null=True, blank=True)
    grammatikes_gnoseis = models.CharField(max_length=50, choices=GRAMMATIKES_GNOSEIS_CHOICES, verbose_name="ΓΡΑΜΜΑΤΙΚΕΣ ΓΝΩΣΕΙΣ", null=True, blank=True)
    eidikes_grammatikes_gnoseis = models.CharField(max_length=255, verbose_name="ΕΙΔΙΚΕΣ ΓΝΩΣΕΙΣ", null=True, blank=True)
    deksiotites = models.TextField(blank=True, null=True, verbose_name="ΔΕΞΙΟΤΗΤΕΣ")
    xenes_glosses = models.CharField(max_length=255, verbose_name="ΞΕΝΕΣ ΓΛΩΣΣΕΣ", null=True, blank=True)

    # Στρατιωτικά Στοιχεία
    asm = models.PositiveIntegerField(verbose_name="ΑΣΜ", default=0)
    vathmos = models.CharField(max_length=10, choices=VATHMOS_CHOICES, verbose_name="ΒΑΘΜΟΣ", null=True, blank=True)
    esso_katataksis = models.CharField(max_length=10, verbose_name="ΕΣΣΟ ΚΑΤΑΤΑΞΗΣ", null=True, blank=True)
    diarkeia_thiteias = models.IntegerField(verbose_name="ΔΙΑΡΚΕΙΑ ΘΗΤΕΙΑΣ (ΜΗΝΕΣ)", null=True, blank=True)
    imerominia_eisodou_monada = models.DateField(verbose_name="ΗΜ. ΕΙΣΟΔΟΥ ΣΤΗΝ ΜΟΝΑΔΑ", null=True, blank=True)
    imerominia_strateusis = models.DateField(verbose_name="ΗΜ. ΣΤΡΑΤΕΥΣΗΣ", null=True, blank=True)
    imerominia_apolysis = models.DateField(verbose_name="ΗΜ. ΑΠΟΛΥΣΕΩΣ", null=True, blank=True)
    poines = models.TextField(verbose_name="ΠΟΙΝΕΣ", null=True, blank=True)
    adeies = models.TextField(verbose_name="ΑΔΕΙΕΣ", null=True, blank=True)
    posto = models.CharField(max_length=100, verbose_name="ΠΟΣΤΟ", choices=POSTO_CHOICES, null=True, blank=True)
    genikes_paratiriseis = models.TextField(verbose_name="ΓΕΝΙΚΕΣ ΠΑΡΑΤΗΡΗΣΕΙΣ", null=True, blank=True)

    # Στοιχεία Υγείας
    somatiki_ikanotita = models.CharField(max_length=10, choices=SOMATIKI_IKANOTITA_CHOICES, verbose_name="ΣΩΜΑΤΙΚΗ ΙΚΑΝΟΤΗΤΑ", null=True, blank=True)
    katastasi_ygeias = models.CharField(max_length=100, verbose_name="ΚΑΤΑΣΤΑΣΗ ΥΓΕΙΑΣ", null=True, blank=True)
    omada_aimatos = models.CharField(max_length=3, verbose_name="ΟΜΑΔΑ ΑΙΜΑΤΟΣ", null=True, blank=True)
    paratiriseis_ygeias = models.TextField(blank=True, null=True, verbose_name="ΠΑΡΑΤΗΡΗΣΕΙΣ ΥΓΕΙΑΣ")

    def __str__(self):
        return f"{self.eponymo} {self.onoma}"

    class Meta:
        verbose_name = _('Οργάνωση | Στρατιώτης')
        verbose_name_plural = _('Οργάνωση | Στρατιώτες')

class AxypKepikServiceReport(models.Model):
    pdf = models.FileField(upload_to='axyp_anafora/', blank=True, null=True)

    def __str__(self):
        if self.pdf:
            return f"Αναφορά ΑΞΥΠ: {self.pdf.name}"
        return "Αναφορά ΑΞΥΠ χωρίς ημερομηνία"
    
    class Meta:
        verbose_name = _('Αναφορά | Αναφορά Αξιωματικού Υπηρεσίας')
        verbose_name_plural = _('Αναφορές | Αναφορές Αξιωματικού Υπηρεσίας')

class OplitiServiceReport(models.Model):
    pdf = models.FileField(upload_to='opliti_reports/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pdf:
            # Δημιουργία του νέου ονόματος αρχείου
            report_date = datetime.now().strftime('%d-%m-%Y')
            new_filename = f'Αναφορά_Οπλίτη_της_{report_date}.pdf'
            self.pdf.name = new_filename
        
        super(OplitiServiceReport, self).save(*args, **kwargs)

    def __str__(self):
        if self.pdf:
            return f"Αναφορά Οπλίτη της {datetime.now().strftime('%d-%m-%Y')}"
        return "Αναφορά Οπλίτη χωρίς ημερομηνία"

    class Meta:
        verbose_name = _('Αναφορά | Αναφορά Οπλίτη Υπηρεσίας')
        verbose_name_plural = _('Αναφορές | Αναφορές Οπλιτών Υπηρεσίας')

class AxypCodesCategory(models.Model):
    # Κατηγορίες για το "ΕΙΔΟΣ"
    ITEM_CHOICES = [
        ('computers', 'ΥΠΟΛΟΓΙΣΤΕΣ'),
        ('pyrseia', 'ΠΥΡΣΕΙΑ'),
        ('applications', 'ΛΟΙΠΕΣ ΕΦΑΡΜΟΓΕΣ'),
        ('staff', 'ΣΤΕΛΕΧΗ'),
        ('useful_phones', 'ΧΡΗΣΙΜΑ ΤΗΛΕΦΩΝΑ'),
        ('phone_codes', 'ΚΩΔΙΚΟΙ ΛΕΙΤΟΥΡΓΙΑΣ ΤΗΛΕΦΩΝΟΥ'),
    ]
    
    # Το βασικό πεδίο για το είδος
    item_type = models.CharField(_('ΕΙΔΟΣ'), max_length=50, choices=ITEM_CHOICES, blank=True, null=True)

    # Πεδία για "ΥΠΟΛΟΓΙΣΤΕΣ", "ΠΥΡΣΕΙΑ", "ΛΟΙΠΕΣ ΕΦΑΡΜΟΓΕΣ"
    server_pc = models.CharField(_('Server/PC'), max_length=100, blank=True, null=True)
    username = models.CharField(_('Username'), max_length=100, blank=True, null=True)
    password = models.CharField(_('Password'), max_length=100, blank=True, null=True)

    # Πεδία για "ΣΤΕΛΕΧΗ"
    last_name = models.CharField(_('Επώνυμο'), max_length=100, blank=True, null=True)
    first_name = models.CharField(_('Όνομα'), max_length=100, blank=True, null=True)
    position = models.CharField(_('Πόστο'), max_length=100, blank=True, null=True)

    # Πεδία για "ΧΡΗΣΙΜΑ ΤΗΛΕΦΩΝΑ"
    description = models.CharField(_('Περιγραφή'), max_length=100, blank=True, null=True)
    contact_phone = models.CharField(_('Τηλέφωνο Επικοινωνίας'), max_length=20, blank=True, null=True)

    # Πεδία για "ΚΩΔΙΚΟΙ ΛΕΙΤΟΥΡΓΙΑΣ ΤΗΛΕΦΩΝΟΥ"
    phone_code = models.CharField(_('Κωδικός'), max_length=50, blank=True, null=True)
    phone_function = models.CharField(_('Λειτουργία'), max_length=100, blank=True, null=True)

    # Γενικό πεδίο για παρατηρήσεις
    notes = models.TextField(_('Παρατηρήσεις'), blank=True, null=True)

    def __str__(self):
        return f'{self.item_type}'

    class Meta:
        verbose_name = _('Κωδικοί ΑΞΥΠ | Όλοι')
        verbose_name_plural = _('Κωδικοί ΑΞΥΠ | Όλοι')

class ServiceReportSummary(models.Model):
    report_date = models.DateField()
    total_sda = models.IntegerField()  # Σύνολο για ΣΔΑ - ΠΥΡΣΕΙΑ
    total_aifs = models.IntegerField()  # Σύνολο για AIFS
    total_cronos = models.IntegerField()  # Σύνολο για CRONOS
    total_general = models.IntegerField()  # Γενικό Σύνολο

    def __str__(self):
        return f"Αναφορά {self.report_date} - Γενικό Σύνολο: {self.total_general}"

class AxypCodesComputers(AxypCodesCategory):
    class Meta:
        proxy = True
        verbose_name = "Κωδικοί ΑΞΥΠ | Υπολογιστές"
        verbose_name_plural = "Κωδικοί ΑΞΥΠ | Υπολογιστές"

class AxypCodesPyrseia(AxypCodesCategory):
    class Meta:
        proxy = True
        verbose_name = "Κωδικοί ΑΞΥΠ | Πυρσεία"
        verbose_name_plural = "Κωδικοί ΑΞΥΠ | Πυρσεία"

class AxypCodesApplications(AxypCodesCategory):
    class Meta:
        proxy = True
        verbose_name = "Κωδικοί ΑΞΥΠ | Λοιπές Εφαρμογές"
        verbose_name_plural = "Κωδικοί ΑΞΥΠ | Λοιπές Εφαρμογές"

class AxypCodesStaff(AxypCodesCategory):
    class Meta:
        proxy = True
        verbose_name = "Κωδικοί ΑΞΥΠ | Στελέχη"
        verbose_name_plural = "Κωδικοί ΑΞΥΠ | Στελέχη"

class AxypCodesUsefulPhones(AxypCodesCategory):
    class Meta:
        proxy = True
        verbose_name = "Κωδικοί ΑΞΥΠ | Χρήσιμα Τηλέφωνα"
        verbose_name_plural = "Κωδικοί ΑΞΥΠ | Χρήσιμα Τηλέφωνα"

class AxypCodesPhoneCodes(AxypCodesCategory):
    class Meta:
        proxy = True
        verbose_name = "Κωδικοί ΑΞΥΠ | Κωδικοί Λειτουργίας Τηλεφώνου"
        verbose_name_plural = "Κωδικοί ΑΞΥΠ | Κωδικοί Λειτουργίας Τηλεφώνου"
        
class KlistoTilefoniko(models.Model):
    CATEGORIES = [
        ('ΥΠΕΘΑ', 'ΥΠΕΘΑ'),
        ('ΓΕΕΘΑ', 'ΓΕΕΘΑ'),
        ('ΓΕΣ', 'ΓΕΣ'),
        ('ΓΕΝ', 'ΓΕΝ'),
        ('ΓΕΑ', 'ΓΕΑ'),
        ('ΚΥΠΡΟΣ', 'ΚΥΠΡΟΣ'),
    ]

    category = models.CharField(max_length=10, choices=CATEGORIES, verbose_name="Κατηγορία")
    stoixeia = models.CharField(max_length=255, verbose_name="Στοιχεία")
    number = models.CharField(max_length=4, verbose_name="Νούμερο")

    def __str__(self):
        return f"{self.category} - {self.stoixeia}"

    class Meta:
        verbose_name = _('Κατάλογος | Κλειστό Τηλεφωνικό')
        verbose_name_plural = _('Κατάλογος | Κλειστό Τηλεφωνικό')

class VOSIPTelephoneDirectory(models.Model):
    EPITELEIO_CHOICES = [
        ('ΓΕΕΘΑ/ΔΕΠ', 'ΓΕΕΘΑ/ΔΕΠ'),
        ('ΓΕΣ', 'ΓΕΣ'),
        ('1 ΣΤΡΑΤΙΑ', '1 ΣΤΡΑΤΙΑ'),
        ('ΑΣΔΕΝ', 'ΑΣΔΕΝ'),
        ('ΑΣΔΥΣ', 'ΑΣΔΥΣ'),
        ('Γ΄ ΣΣ', 'Γ΄ ΣΣ'),
        ('Δ΄ ΣΣ', 'Δ΄ ΣΣ'),
        ('Ι ΜΠ', 'Ι ΜΠ'),
        ('ΔΔΕΕ', 'ΔΔΕΕ'),
        ('ΙΙ Μ/Κ ΜΠ', 'ΙΙ Μ/Κ ΜΠ'),
        ('XII M/K MΠ', 'XII M/K MΠ'),
        ('XVI M/K MΠ', 'XVI M/K MΠ'),
        ('ΧΧ ΤΘΜ', 'ΧΧ ΤΘΜ'),
        ('95 ΑΔΤΕ', '95 ΑΔΤΕ'),
        ('98 ΑΔΤΕ', '98 ΑΔΤΕ'),
        ('3 Μ/Κ ΤΑΞ', '3 Μ/Κ ΤΑΞ'),
        ('7 Μ/Κ ΤΑΞ', '7 Μ/Κ ΤΑΞ'),
        ('30 Μ/Κ ΤΑΞ', '30 Μ/Κ ΤΑΞ'),
        ('31 Μ/Κ ΤΑΞ', '31 Μ/Κ ΤΑΞ'),
        ('33 Μ/Κ ΤΑΞ', '33 Μ/Κ ΤΑΞ'),
        ('34 Μ/Κ ΤΑΞ', '34 Μ/Κ ΤΑΞ'),
        ('50 Μ/Κ ΤΑΞ', '50 Μ/Κ ΤΑΞ'),
        ('8 Μ/Π ΤΑΞ', '8 Μ/Π ΤΑΞ'),
        ('9 Μ/Π ΤΑΞ', '9 Μ/Π ΤΑΞ'),
        ('29 Μ/Π ΤΑΞ', '29 Μ/Π ΤΑΞ'),
        ('5 ΤΑΞΠΖ', '5 ΤΑΞΠΖ'),
        ('1 ΤΑΞΚΔ-ΑΛ', '1 ΤΑΞΚΔ-ΑΛ'),
        ('32 ΤΑΞΠΝ', '32 ΤΑΞΠΝ'),
        ('71 Α/Μ ΤΑΞ', '71 Α/Μ ΤΑΞ'),
        ('ΧΧΙ ΤΘΤ', 'ΧΧΙ ΤΘΤ'),
        ('ΧΧΙΙΙ ΤΘΤ', 'ΧΧΙΙΙ ΤΘΤ'),
        ('ΧΧΙV ΤΘΤ', 'ΧΧΙV ΤΘΤ'),
        ('ΧΧV ΤΘΤ', 'ΧΧV ΤΘΤ'),
        ('1Η ΤΑΞΑΣ', '1Η ΤΑΞΑΣ'),
        ('79 ΑΔΤΕ', '79 ΑΔΤΕ'),
        ('80 ΑΔΤΕ', '80 ΑΔΤΕ'),
        ('96 ΑΔΤΕ', '96 ΑΔΤΕ'),
        ('88 ΣΔΙ', '88 ΣΔΙ'),
        ('ΤΔ/21 Μ/Κ ΣΠ', 'ΤΔ/21 Μ/Κ ΣΠ'),
        ('ΤΔ/41 ΣΠ', 'ΤΔ/41 ΣΠ'),
        ('1 ΣΠ', '1 ΣΠ'),
        ('10 ΣΠ', '10 ΣΠ'),
        ('15 ΣΠ', '15 ΣΠ'),
        ('ΕΛΔΥΚ', 'ΕΛΔΥΚ'),
        ('487 ΤΔΒ', '487 ΤΔΒ'),
    ]
        
    epiteleio_sximatismos = models.CharField(max_length=255, choices=EPITELEIO_CHOICES, verbose_name="Επιτελείο - Σχηματισμός")
    xristis = models.CharField(max_length=255, verbose_name="Χρήστης")
    arithmos_vosip = models.CharField(max_length=255, blank=True, null=True, verbose_name="Αριθμός VoSIP")
    paratiriseis = models.TextField(blank=True, null=True, verbose_name="Παρατηρήσεις")

    def __str__(self):
        return f"{self.epiteleio_sximatismos} - {self.xristis}"

    class Meta:
        verbose_name = _('Κατάλογος | VOSIP')
        verbose_name_plural = _('Κατάλογος | VOSIP')

class HARPDirectory(models.Model):
    # Define the choices for Επιτελείο - Σχηματισμός
    EPITELEIO_CHOICES = [
        ('ΥΠΕΘΑ', 'ΥΠΕΘΑ'),
        ('ΓΕΕΘΑ', 'ΓΕΕΘΑ'),
        ('ΓΕΣ', 'ΓΕΣ'),
        ('1η ΣΤΡΑΤΙΑ', '1η ΣΤΡΑΤΙΑ'),
        ('ΓΣΣ', 'ΓΣΣ'),
        ('ΔΣΣ', 'ΔΣΣ'),
        ('ΑΣΔΕΝ', 'ΑΣΔΕΝ'),
        ('ΑΣΔΥΣ', 'ΑΣΔΥΣ'),
        ('I ΜΠ', 'I ΜΠ'),
        ('ΓΕΝ', 'ΓΕΝ'),
        ('ΓΕΑ', 'ΓΕΑ'),
    ]

    epiteleio_sximatismos = models.CharField(
        max_length=255, 
        choices=EPITELEIO_CHOICES,
        verbose_name='Επιτελείο - Σχηματισμός'
    )
    aa_ana_sximatismo = models.CharField(max_length=255, verbose_name='Α/Α (ανα σχηματισμό)')
    antapokritis = models.CharField(max_length=255, verbose_name='Ανταποκριτής')
    arithmos_sip = models.CharField(max_length=255, verbose_name='Αριθμός SIP')
    syskeyi = models.CharField(max_length=255, verbose_name='Συσκευή')

    def __str__(self):
        return f"{self.epiteleio_sximatismos} - {self.antapokritis}"

    class Meta:
        verbose_name = 'Κατάλογος | HARP'
        verbose_name_plural = 'Κατάλογος | HARP'

class ErmisDirectory(models.Model):
    # Define the choices for Επιτελείο - Σχηματισμός
    EPITELEIO_CHOICES = [
        ('ΓΕΕΘΑ - ΓΕΣ', 'ΓΕΕΘΑ - ΓΕΣ'),
        ('1η ΣΤΡΑΤΙΑ', '1η ΣΤΡΑΤΙΑ'),
        ('Ι ΜΠ', 'Ι ΜΠ'),
        ('32 ΤΑΞΠ/Ν', '32 ΤΑΞΠ/Ν'),
        ('71 Α/Μ ΤΑΞ', '71 Α/Μ ΤΑΞ'),
        ('1 ΤΑΞΑΣ', '1 ΤΑΞΑΣ'),
        ('1 ΤΑΞΚΔ-ΑΛ', '1 ΤΑΞΚΔ-ΑΛ'),
        ('ΙI Μ/Κ ΜΠ', 'ΙI Μ/Κ ΜΠ'),
        ('33 Μ/Κ ΤΑΞ', '33 Μ/Κ ΤΑΞ'),
        ('34 Μ/Κ ΤΑΞ', '34 Μ/Κ ΤΑΞ'),
        ('Γ΄ΣΣ / NDC-GR', 'Γ΄ΣΣ / NDC-GR'),
        ('8 M/Π ΤΑΞ', '8 M/Π ΤΑΞ'),
        ('9 ΤΑΞΠΖ', '9 ΤΑΞΠΖ'),
        ('10 ΣΠ «Χ ΜΠ»', '10 ΣΠ «Χ ΜΠ»'),
        ('Δ΄ ΣΣ', 'Δ΄ ΣΣ'),
        ('ΧΙΙ Μ/Κ ΜΠ', 'ΧΙΙ Μ/Κ ΜΠ'),
        ('7 Μ/Κ ΤΑΞ', '7 Μ/Κ ΤΑΞ'),
        ('31 Μ/Κ ΤΑΞ', '31 Μ/Κ ΤΑΞ'),
        ('ΧΧΙΙΙ ΤΘΤ', 'ΧΧΙΙΙ ΤΘΤ'),
        ('50 Μ/Κ ΤΑΞ', '50 Μ/Κ ΤΑΞ'),
        ('XVΙ Μ/Κ ΜΠ', 'XVΙ Μ/Κ ΜΠ'),
        ('3 Μ/Κ ΤΑΞ', '3 Μ/Κ ΤΑΞ'),
        ('30 Μ/Κ ΤΑΞ', '30 Μ/Κ ΤΑΞ'),
        ('ΤΔ/21 ΣΠ', 'ΤΔ/21 ΣΠ'),
        ('ΧΧ ΤΘΜ', 'ΧΧ ΤΘΜ'),
        ('ΧΧΙ ΤΘΤ', 'ΧΧΙ ΤΘΤ'),
        ('XXIV ΤΘΤ', 'XXIV ΤΘΤ'),
        ('ΧΧV ΤΘΤ', 'ΧΧV ΤΘΤ'),
        ('29 ΤΑΞΠΖ', '29 ΤΑΞΠΖ'),
        ('IV ΤΑΞΥΠ', 'IV ΤΑΞΥΠ'),
        ('1 ΣΠΒ (MLRS)', '1 ΣΠΒ (MLRS)'),
        ('473 ΤΕΠΠ/ΛΜΕΑ', '473 ΤΕΠΠ/ΛΜΕΑ'),
        ('AΣΔΕΝ', 'AΣΔΕΝ'),
        ('ΤΔ/41 ΣΠ', 'ΤΔ/41 ΣΠ'),
        ('95 ΑΔΤΕ', '95 ΑΔΤΕ'),
        ('ΔΑΝ ΜΕΓΙΣΤΗΣ', 'ΔΑΝ ΜΕΓΙΣΤΗΣ'),
        ('549 ΤΕ', '549 ΤΕ'),
        ('98 ΑΔΤΕ', '98 ΑΔΤΕ'),
        ('96 ΑΔΤΕ', '96 ΑΔΤΕ'),
        ('79 ΑΔΤΕ', '79 ΑΔΤΕ'),
        ('ΔΑΝ ΙΚΑΡΙΑΣ', 'ΔΑΝ ΙΚΑΡΙΑΣ'),
        ('80 ΑΔΤΕ', '80 ΑΔΤΕ'),
        ('5/42 ΣΕ', '5/42 ΣΕ'),
        ('88 ΣΔΙ', '88 ΣΔΙ'),
        ('ΣΔΒ-472 ΤΕΠΠ', 'ΣΔΒ-472 ΤΕΠΠ'),
        ('ΜΕΡΥΠ', 'ΜΕΡΥΠ'),
        ('ΓΕΝ', 'ΓΕΝ'),
        ('ΑΡΧΗΓΕΙΟ ΣΤΟΛΟΥ', 'ΑΡΧΗΓΕΙΟ ΣΤΟΛΟΥ'),
        ('ΣΔΑΜ', 'ΣΔΑΜ'),
        ('ΣΔΑΜ - ΕΘΚΕΠΙΧ', 'ΣΔΑΜ - ΕΘΚΕΠΙΧ'),
        ('ΓΕA', 'ΓΕA'),
        ('ATA', 'ATA'),
        ('130 ΣΜ', '130 ΣΜ'),
        ('135 ΣΜ', '135 ΣΜ'),
        ('ΔΙΜΥΠΕ', 'ΔΙΜΥΠΕ'),
    ]

    # Επιτελείο - Σχηματισμός με επιλογές
    epiteleio_sximatismos = models.CharField(
        max_length=255, 
        choices=EPITELEIO_CHOICES,
        verbose_name='Επιτελείο - Σχηματισμός'
    )

    katigoria = models.CharField(max_length=255, verbose_name='Κατηγορία')
    antapokritis = models.CharField(max_length=255, verbose_name='Ανταποκριτής')
    arithmos_call = models.CharField(max_length=255, verbose_name='Αριθμός Κλήσεως')

    def __str__(self):
        return f"{self.epiteleio_sximatismos} - {self.katigoria} - {self.antapokritis}"

    class Meta:
        verbose_name = 'Κατάλογος | ΣΑΖΜ - ΕΡΜΗΣ'
        verbose_name_plural = 'Κατάλογος | ΣΑΖΜ - ΕΡΜΗΣ'

class FCTDirectory(models.Model):
    fct_call_center = models.CharField(max_length=255, verbose_name='Τηλεφωνικό Κέντρο')
    arithmos_fct = models.CharField(max_length=255, verbose_name='Αριθμός')
    vpn_fct = models.CharField(max_length=255, verbose_name='VPN')

    def __str__(self):
        return f"{self.fct_call_center} - {self.arithmos_fct} - {self.vpn_fct}"

    class Meta:
        verbose_name = 'Κατάλογος | FCT'
        verbose_name_plural = 'Κατάλογος | FCT'

class YpaspistirioDirectory(models.Model):
    antapokritis = models.CharField(max_length=255, verbose_name='Ανταποκριτής')
    arithmos_ypasp = models.CharField(max_length=255, verbose_name='Αριθμός')

    def __str__(self):
        return f"{self.antapokritis} - {self.arithmos_ypasp}"

    class Meta:
        verbose_name = 'Κατάλογος | Υπασπιστήρια Ιεραρχίας'
        verbose_name_plural = 'Κατάλογος | Υπασπιστήρια Ιεραρχίας'

class SeclineDirectory(models.Model):
    antapokritis = models.CharField(max_length=255, verbose_name='Ανταποκριτής')
    arithmos_ote = models.CharField(max_length=255, verbose_name='Αριθμός ΟΤΕ')
    arithmos_epsad = models.CharField(max_length=255, verbose_name='Αριθμός ΕΨΑΔ')
    paratiriseis = models.CharField(max_length=255, verbose_name='Παρατηρήσεις')

    def __str__(self):
        return f"{self.antapokritis} - {self.arithmos_ote} - {self.arithmos_epsad} - {self.paratiriseis} "

    class Meta:
        verbose_name = 'Κατάλογος | Secline Plus-STU II'
        verbose_name_plural = 'Κατάλογος | Secline Plus-STU II'

class SOSDirectory(models.Model):
    # Define the choices for Επιτελείο - Σχηματισμός
    EPITELEIO_CHOICES = [
        ('Γενικό Επιτελείο Εθνικής Άμυνας', 'Γενικό Επιτελείο Εθνικής Άμυνας'),
        ('ΔΕΠ', 'ΔΕΠ'),
        ('Στρατός Ξηράς', 'Στρατός Ξηράς'),
        ('Πολεμικό Ναυτικό', 'Πολεμικό Ναυτικό'),
        ('Πολεμική Αεροπορία', 'Πολεμική Αεροπορία'),
    ]

    epiteleio_sximatismos = models.CharField(
        max_length=255, 
        choices=EPITELEIO_CHOICES,
        verbose_name='Επιτελείο - Σχηματισμός'
    )
    aa_ana_sximatismo = models.CharField(max_length=255, verbose_name='Α/Α (ανα σχηματισμό)')
    klados_ypiresia = models.CharField(max_length=255, verbose_name='Κλάδος - Υπηρεσία')
    thl_syndesh = models.CharField(max_length=255, verbose_name='Αριθμός Τηλεφωνικής Σύνδεσης')

    def __str__(self):
        return f"{self.epiteleio_sximatismos} - {self.aa_ana_sximatismo} - {self.klados_ypiresia} - {self.thl_syndesh}"

    class Meta:
        verbose_name = 'Κατάλογος | Δίκτυο Έκτακτων Αναγκών'
        verbose_name_plural = 'Κατάλογος | Δίκτυο Έκτακτων Αναγκών'

class DailyService(models.Model):
    SERVICE_TYPES = [
        ('ΕΞ', 'ΕΞ'),          # Έξοδος
        ('ΤΗΠ', 'ΤΗΠ'),        # Τηλεπικοινωνίες
        ('ΑΔΕΙΑ', 'ΑΔΕΙΑ'),    # Άδεια
        ('ΑΝΤΑΠΟΚΡΙΣΗ', 'ΑΝΤΑΠΟΚΡΙΣΗ'),  # Ανταπόκριση
        # Πρόσθεσε άλλους τύπους υπηρεσιών αν χρειάζεται
    ]

    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    date = models.DateField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, blank=True, null=True)

    class Meta:
        unique_together = ('soldier', 'date')
        verbose_name = _('Ημερήσια Υπηρεσία')
        verbose_name_plural = _('Ημερήσιες Υπηρεσίες')

    def __str__(self):
        return f"{self.soldier} - {self.date}: {self.get_service_type_display()}"