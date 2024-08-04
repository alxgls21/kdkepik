# myapp/admin.py

from django.contrib import admin
from .models import DidesCategory, HarpCategory, AdmeCategory

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

admin.site.register(DidesCategory, DidesCategoryAdmin)
admin.site.register(HarpCategory, HarpCategoryAdmin)
admin.site.register(AdmeCategory, AdmeCategoryAdmin)
