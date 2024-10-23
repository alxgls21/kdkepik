from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import DidesCategory, HarpCategory, AdmeCategory, OfficerServiceReport, Soldier, AxypKepikServiceReport, OplitiServiceReport, AxypCodesCategory, AxypCodesComputers, AxypCodesPyrseia, AxypCodesApplications,  AxypCodesStaff, AxypCodesUsefulPhones, AxypCodesPhoneCodes, KlistoTilefoniko, VOSIPTelephoneDirectory, HARPDirectory, ErmisDirectory, FCTDirectory, YpaspistirioDirectory, SeclineDirectory, SOSDirectory

class DidesCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'application', 'ip_address', 'supervisory_tool')
    list_filter = ('category', 'application')
    search_fields = ('name', 'ip_address', 'supervisory_tool')

class HarpCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'supervisory_tool')
    search_fields = ('name', 'ip_address', 'supervisory_tool')

class AdmeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'supervisory_tool')
    search_fields = ('name', 'ip_address', 'supervisory_tool')

class OfficerServiceReportAdmin(admin.ModelAdmin):
    list_display = ('rank', 'last_name', 'first_name', 'phone_number')
    search_fields = ('rank', 'last_name', 'first_name', 'phone_number')
    list_filter = ('rank',)
    
class SoldierAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Προσωπικά Στοιχεία', {
            'fields': (
                'eponymo', 'onoma', 'etos_genniseos', 'topos_genniseos',
                'onoma_patros', 'epaggelma_patros', 'onoma_mitros', 'epaggelma_mitros',
                'tilefono_kinito', 'tilefono_stathero', 'tilefono_oikeiou', 'oikeiou_sxesi',
                'topos_katagogis', 'topos_diamonis', 'periochi', 'odos_arithmos',
                'oikogeneiaki_katastasi', 'arithmos_adelfon', 'oikonomiki_katastasi',
            )
        }),
        ('Εκπαίδευση και Επάγγελμα', {
            'fields': (
                'epaggelma_politis', 'grammatikes_gnoseis', 'eidikes_grammatikes_gnoseis',
                'deksiotites', 'xenes_glosses'
            )
        }),
        ('Στρατιωτικά Στοιχεία', {
            'fields': (
                'asm', 'vathmos', 'esso_katataksis', 'diarkeia_thiteias',
                'imerominia_eisodou_monada', 'imerominia_strateusis', 'imerominia_apolysis',
                'poines', 'adeies', 'posto', 'genikes_paratiriseis'
            )
        }),
        ('Στοιχεία Υγείας', {
            'fields': (
                'somatiki_ikanotita', 'katastasi_ygeias', 'omada_aimatos', 'paratiriseis_ygeias'
            )
        }),
    )

    list_display = ('vathmos','eponymo', 'onoma', 'posto', 'imerominia_apolysis')
    search_fields = ('vathmos', 'eponymo', 'onoma')
    list_filter = ('vathmos', 'somatiki_ikanotita')

class AxypCodesCategoryAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'server_pc', 'username', 'notes')
    search_fields = ('item_type', 'username', 'last_name', 'description', 'phone_code')

    class Media:
        js = ('js/axypcodes.js',)

class ComputersAdmin(AxypCodesCategoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(item_type='computers')

class PyrseiaAdmin(AxypCodesCategoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(item_type='pyrseia')

class ApplicationsAdmin(AxypCodesCategoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(item_type='applications')

class StaffAdmin(AxypCodesCategoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(item_type='staff')

class UsefulPhonesAdmin(AxypCodesCategoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(item_type='useful_phones')

class PhoneCodesAdmin(AxypCodesCategoryAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(item_type='phone_codes')

class KlistoTilefonikoAdmin(admin.ModelAdmin):
    list_display = ('category', 'stoixeia', 'number')
    search_fields = ('stoixeia', 'category')
    
class VOSIPTelephoneDirectoryAdmin(admin.ModelAdmin):
    list_display = ('epiteleio_sximatismos', 'xristis', 'arithmos_vosip', 'paratiriseis')
    search_fields = ('epiteleio_sximatismos', 'xristis', 'arithmos_vosip')
    
class HARPDirectoryAdmin(admin.ModelAdmin):
    list_display = ['epiteleio_sximatismos', 'aa_ana_sximatismo', 'antapokritis', 'arithmos_sip', 'syskeyi']
    search_fields = ['epiteleio_sximatismos', 'antapokritis', 'arithmos_sip']

class ErmisDirectoryAdmin(admin.ModelAdmin):
    list_display = ['epiteleio_sximatismos', 'katigoria', 'antapokritis', 'arithmos_call']
    search_fields = ['epiteleio_sximatismos', 'antapokritis', 'arithmos_call']

class FCTDirectoryAdmin(admin.ModelAdmin):
    list_display = ['fct_call_center', 'arithmos_fct', 'vpn_fct']
    search_fields = ['fct_call_center', 'arithmos_fct', 'vpn_fct']

class YpaspistirioDirectoryAdmin(admin.ModelAdmin):
    list_display = ['antapokritis', 'arithmos_ypasp']
    search_fields = ['antapokritis', 'arithmos_ypasp']

class SeclineDirectoryAdmin(admin.ModelAdmin):
    list_display = ['antapokritis', 'arithmos_ote', 'arithmos_epsad', 'paratiriseis']
    search_fields = ['antapokritis', 'arithmos_ote', 'arithmos_epsad', 'paratiriseis']

class SOSDirectoryAdmin(admin.ModelAdmin):
    list_display = ['epiteleio_sximatismos', 'aa_ana_sximatismo', 'klados_ypiresia', 'thl_syndesh']
    search_fields = ['epiteleio_sximatismos', 'aa_ana_sximatismo', 'klados_ypiresia', 'thl_syndesh']

admin.site.register(DidesCategory, DidesCategoryAdmin)
admin.site.register(HarpCategory, HarpCategoryAdmin)
admin.site.register(AdmeCategory, AdmeCategoryAdmin)
admin.site.register(OfficerServiceReport, OfficerServiceReportAdmin)
admin.site.register(Soldier, SoldierAdmin)
admin.site.register(AxypKepikServiceReport)
admin.site.register(OplitiServiceReport)
admin.site.register(AxypCodesCategory, AxypCodesCategoryAdmin)
admin.site.register(AxypCodesComputers, ComputersAdmin)
admin.site.register(AxypCodesPyrseia, PyrseiaAdmin)
admin.site.register(AxypCodesApplications, ApplicationsAdmin)
admin.site.register(AxypCodesStaff, StaffAdmin)
admin.site.register(AxypCodesUsefulPhones, UsefulPhonesAdmin)
admin.site.register(AxypCodesPhoneCodes, PhoneCodesAdmin)
admin.site.register(KlistoTilefoniko, KlistoTilefonikoAdmin)
admin.site.register(VOSIPTelephoneDirectory, VOSIPTelephoneDirectoryAdmin)
admin.site.register(HARPDirectory, HARPDirectoryAdmin)
admin.site.register(ErmisDirectory, ErmisDirectoryAdmin)
admin.site.register(FCTDirectory, FCTDirectoryAdmin)
admin.site.register(YpaspistirioDirectory, YpaspistirioDirectoryAdmin)
admin.site.register(SeclineDirectory, SeclineDirectoryAdmin)
admin.site.register(SOSDirectory, SOSDirectoryAdmin)