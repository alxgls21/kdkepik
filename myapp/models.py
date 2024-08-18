# myapp/models.py

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


class AxypKepikServiceReport(models.Model):
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pdf:
            # Δημιουργία του νέου ονόματος αρχείου
            report_date = datetime.now().strftime('%d-%m-%Y')
            new_filename = f'Αναφορά_ΑΞΥΠ_της_{report_date}.pdf'
            self.pdf.name = new_filename
        
        super(AxypKepikServiceReport, self).save(*args, **kwargs)

    def __str__(self):
        if self.pdf:
            return f"Αναφορά ΑΞΥΠ της {datetime.now().strftime('%d-%m-%Y')}"
        return "Αναφορά ΑΞΥΠ χωρίς ημερομηνία"
    
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