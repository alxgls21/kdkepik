# myapp/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

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
        verbose_name = _('ΔΙΔΕΣ')
        verbose_name_plural = _('ΔΙΔΕΣ')

class HarpCategory(models.Model):
    name = models.CharField(_('Όνομα'), max_length=100)
    ip_address = models.URLField(_('Διεύθυνση IP'), blank=True, null=True)  # Χρήση URLField για πλήρη URLs
    supervisory_tool = models.CharField(_('Εποπτικό Μέσο'), max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('HARP')
        verbose_name_plural = _('HARP')

class AdmeCategory(models.Model):
    name = models.CharField(_('Όνομα'), max_length=100)
    ip_address = models.URLField(_('Διεύθυνση IP'), blank=True, null=True)  # Χρήση URLField για πλήρη URLs
    supervisory_tool = models.CharField(_('Εποπτικό Μέσο'), max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('ΑΔΜΕ')
        verbose_name_plural = _('ΑΔΜΕ')

class OfficerServiceReport(models.Model):
    rank = models.CharField(_('Βαθμός'), max_length=50)
    last_name = models.CharField(_('Επώνυμο'), max_length=100)
    first_name = models.CharField(_('Όνομα'), max_length=100)
    phone_number = models.CharField(_('Τηλ Επικοινωνίας'), max_length=15)

    class Meta:
        verbose_name = _('Αξιωματικός Υπηρεσίας ΚΕΠΙΚ')
        verbose_name_plural = _('Αξιωματικοί Υπηρεσίας ΚΕΠΙΚ')

    def __str__(self):
        return f'{self.rank} {self.last_name} {self.first_name}'
    
class Soldier(models.Model):
    RANK_CHOICES = [
        ('ΣΤΡ(ΔΒ)', 'ΣΤΡ(ΔΒ)'),
    ]

    rank = models.CharField(_('Βαθμός'), max_length=50, choices=RANK_CHOICES)
    asm = models.CharField(_('ΑΣΜ'), max_length=50)
    enlistment_esso = models.CharField(_('ΕΣΣΟ Κατάταξης'), max_length=50)
    last_name = models.CharField(_('Επώνυμο'), max_length=100)
    first_name = models.CharField(_('Όνομα'), max_length=100)
    discharge_date = models.DateField(_('Ημερομηνία Απολύσεως'))
    
    physical_ability = models.CharField(_('Σωματική Ικανότητα'), max_length=50, blank=True, null=True)
    birth_year = models.IntegerField(_('Έτος Γέννησης'), blank=True, null=True)
    birth_place = models.CharField(_('Τόπος Γέννησης'), max_length=100, blank=True, null=True)
    father_name = models.CharField(_('Όνομα Πατέρα'), max_length=100, blank=True, null=True)
    father_occupation = models.CharField(_('Επάγγελμα Πατέρα'), max_length=100, blank=True, null=True)
    mother_name = models.CharField(_('Όνομα Μητέρας'), max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(_('Επάγγελμα Μητέρας'), max_length=100, blank=True, null=True)
    origin_place = models.CharField(_('Τόπος Καταγωγής'), max_length=100, blank=True, null=True)
    residence_place = models.CharField(_('Τόπος Διαμονής'), max_length=100, blank=True, null=True)
    area = models.CharField(_('Περιοχή'), max_length=100, blank=True, null=True)
    street = models.CharField(_('Οδός'), max_length=100, blank=True, null=True)
    street_number = models.CharField(_('Αριθμός'), max_length=10, blank=True, null=True)
    phone_number_home = models.CharField(_('Σταθερό Τηλέφωνο'), max_length=20, blank=True, null=True)
    phone_number_mobile = models.CharField(_('Κινητό Τηλέφωνο'), max_length=20, blank=True, null=True)
    relative_phone = models.CharField(_('Τηλέφωνο Συγγενών'), max_length=20, blank=True, null=True)
    relative_relation = models.CharField(_('Ιδιότητα Συγγενή'), max_length=100, blank=True, null=True)
    occupation = models.CharField(_('Επάγγελμα'), max_length=100, blank=True, null=True)
    special_skills = models.CharField(_('Ειδικές Γνώσεις'), max_length=100, blank=True, null=True)
    education = models.CharField(_('Γραμματικές Γνώσεις'), max_length=100, blank=True, null=True)
    foreign_languages = models.CharField(_('Ξένες Γλώσσες'), max_length=100, blank=True, null=True)
    unit_entry_date = models.DateField(_('Ημ. Εισόδου στην Μονάδα'), blank=True, null=True)
    service_duration = models.IntegerField(_('Διάρκεια θητείας (μήνες)'), blank=True, null=True)
    health_status = models.CharField(_('Κατάσταση Υγείας'), max_length=100, blank=True, null=True)
    blood_type = models.CharField(_('Ομάδα Αίματος'), max_length=10, blank=True, null=True)
    marital_status = models.CharField(_('Οικογενειακή Κατάσταση'), max_length=100, blank=True, null=True)
    siblings_number = models.IntegerField(_('Αριθμός Αδελφών'), blank=True, null=True)
    economic_status = models.CharField(_('Οικονομική Κατάσταση'), max_length=100, blank=True, null=True)
    concerns = models.TextField(_('Προβλήματα που απασχολούν'), blank=True, null=True)
    penalties = models.TextField(_('Ποινές'), blank=True, null=True)
    leaves = models.TextField(_('Άδειες'), blank=True, null=True)

    def __str__(self):
        return f'{self.rank} {self.last_name} {self.first_name}'

    class Meta:
        verbose_name = _('Στρατιώτης')
        verbose_name_plural = _('Στρατιώτες')
        
class Report(models.Model):
    # ΤΙΤΛΟΣ
    date = models.DateField(verbose_name="Ημερομηνία")

    # ΑΞΥΠ ΚΕΠΙΚ
    informed_by_commander_kepik = models.BooleanField(default=False, verbose_name="Ενημερώθηκα απο τον Διοικητή ΚΕΠΙΚ")
    informed_by_company_commander = models.BooleanField(default=False, verbose_name="Ενημερώθηκα από τον Διοικητή Λόχου")
    informed_by_unit_commander = models.BooleanField(default=False, verbose_name="Ενημερώθηκα από τον Διοικητή Μονάδας")
    received_keys = models.BooleanField(default=False, verbose_name="Παρελήφθησαν τα κλειδιά της κλειδοθήκης ΑΞΥΠ ΚΕΠΙΚ")

    # ΤΜΗΜΑ ΤΗΛΕΦΩΝΙΚΟΥ ΚΕΝΤΡΟΥ
    phone_service_soldier = models.ForeignKey(Soldier, related_name='phone_service', on_delete=models.CASCADE, verbose_name="Οπλίτης σε υπηρεσία")
    phone_check_done = models.BooleanField(default=False, verbose_name="Έγινε τηλεφωνικός έλεγχος τις προβλεπόμενες ώρες")
    reported_interruptions = models.TextField(blank=True, verbose_name="Διακοπές που αναφέρθηκαν")
    causes_and_duration = models.TextField(blank=True, verbose_name="Αίτια και διάρκεια διακοπών")
    restoration_actions = models.TextField(blank=True, verbose_name="Ενέργειες αποκατάστασης διακοπών")
    restored_interruptions = models.TextField(blank=True, verbose_name="Διακοπές που αποκαταστήθηκαν")

    # ΤΜΗΜΑ ΚΑΤΑΧΩΡΙΣΗΣ/ΤΗΛΕΤΥΠΩΝ
    teletype_service_soldier = models.ForeignKey(Soldier, related_name='teletype_service', on_delete=models.CASCADE, verbose_name="Οπλίτης σε υπηρεσία")
    system_operation_sda_pyrseia = models.TextField(blank=True, verbose_name="ΣΔΑ - ΠΥΡΣΕΙΑ")
    system_operation_aifs = models.TextField(blank=True, verbose_name="AIFS")
    system_operation_cronos = models.TextField(blank=True, verbose_name="CRONOS")
    fault_restoration_actions = models.TextField(blank=True, verbose_name="Ενέργειες αποκατάστασης βλαβών (αν υπάρχουν)")

    # ΤΜΗΜΑ ΔΙΚΤΥΩΝ
    network_check_done = models.BooleanField(default=False, verbose_name="Έγινε έλεγχος του δικτύου (ΔΙΔΕΣ, NS WAN, ΑΔΜΕ) μέσω των εποπτικών εργαλείων ανά τρίωρο")
    network_problem_found = models.TextField(blank=True, verbose_name="Πρόβλημα που διαπιστώθηκε")

    servers_check_done = models.BooleanField(default=False, verbose_name="Έγινε έλεγχος των εξυπηρετητών του ΚΕΠΙΚ/ΓΕΣ μέσω των εποπτικών εργαλείων ανά τρίωρο")
    servers_problem_found = models.TextField(blank=True, verbose_name="Πρόβλημα που διαπιστώθηκε")

    applications_check_done = models.BooleanField(default=False, verbose_name="Έγινε έλεγχος των εφαρμογών του ΚΕΠΙΚ/ΓΕΣ μέσω των υπερσυνδέσμων ανά τρίωρο")
    applications_problem_found = models.TextField(blank=True, verbose_name="Πρόβλημα που διαπιστώθηκε")

    vosip_check_done = models.BooleanField(default=False, verbose_name="Έγινε έλεγχος των τηλεφώνων VOSIP μέσω των εποπτικών εργαλείων ανά τρίωρο")
    vosip_problem_found = models.TextField(blank=True, verbose_name="Πρόβλημα που διαπιστώθηκε")

    def __str__(self):
        return f"Αναφορά για {self.date}"