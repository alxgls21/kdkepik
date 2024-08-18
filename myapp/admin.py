# myapp/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import DidesCategory, HarpCategory, AdmeCategory, OfficerServiceReport, Soldier, AxypKepikServiceReport, OplitiServiceReport

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
    list_display = ('rank', 'last_name', 'first_name', 'enlistment_esso', 'discharge_date')
    search_fields = ('rank', 'last_name', 'first_name', 'enlistment_esso')
    list_filter = ('rank', 'enlistment_esso')

admin.site.register(DidesCategory, DidesCategoryAdmin)
admin.site.register(HarpCategory, HarpCategoryAdmin)
admin.site.register(AdmeCategory, AdmeCategoryAdmin)
admin.site.register(OfficerServiceReport, OfficerServiceReportAdmin)
admin.site.register(Soldier, SoldierAdmin)
admin.site.register(AxypKepikServiceReport)
admin.site.register(OplitiServiceReport)
