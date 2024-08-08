from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            'date',
            'informed_by_commander_kepik',
            'informed_by_company_commander',
            'informed_by_unit_commander',
            'received_keys',
            'phone_service_soldier',
            'phone_check_done',
            'reported_interruptions',
            'causes_and_duration',
            'restoration_actions',
            'restored_interruptions',
            'teletype_service_soldier',
            'system_operation_sda_pyrseia',
            'system_operation_aifs',
            'system_operation_cronos',
            'fault_restoration_actions',
            'network_check_done',
            'network_problem_found',
            'servers_check_done',
            'servers_problem_found',
            'applications_check_done',
            'applications_problem_found',
            'vosip_check_done',
            'vosip_problem_found',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
