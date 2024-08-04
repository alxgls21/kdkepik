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
