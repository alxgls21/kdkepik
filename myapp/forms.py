from django import forms

class SoldierForm(forms.Form):
    post = forms.CharField(max_length=100, required=False)
    service = forms.CharField(max_length=100, required=False)
    night = forms.CharField(max_length=100, required=False)
    change = forms.CharField(max_length=100, required=False)
    duration = forms.CharField(max_length=100, required=False)
    from_date = forms.DateField(required=False, widget=forms.DateInput(format='%d/%m/%Y'))
    to_date = forms.DateField(required=False, widget=forms.DateInput(format='%d/%m/%Y'))
    cleaning = forms.CharField(max_length=100, required=False)

# Φόρμες για συγκεντρωτικά στοιχεία
class SummaryForm(forms.Form):
    absences = forms.IntegerField(required=False)
    present = forms.IntegerField(required=False)

# Φόρμα για ειδικά στοιχεία
class SpecialDetailsForm(forms.Form):
    honor_leaves = forms.IntegerField(required=False)
    regular_leaves = forms.IntegerField(required=False)
    service_leaves = forms.IntegerField(required=False)
    ey_leaves = forms.IntegerField(required=False)
    detachment = forms.IntegerField(required=False)
    total_special = forms.IntegerField(required=False)

# Φόρμα για υπηρεσία σήμερα και εφεδρικοί
class CurrentServiceForm(forms.Form):
    service_change = forms.CharField(max_length=100, required=False)

# Φόρμα για εξοδούχους
class ExodouchoiForm(forms.Form):
    service = forms.CharField(max_length=100, required=False)
    night = forms.CharField(max_length=100, required=False)

# Φόρμα για κανονικές άδειες
class RegularLeaveForm(forms.Form):
    leave_type = forms.CharField(max_length=100, required=False)
    from_date = forms.CharField(max_length=100, required=False)
    to_date = forms.CharField(max_length=100, required=False)

# Φόρμα για ειδικές περιπτώσεις
class SpecialCaseForm(forms.Form):
    case_type = forms.CharField(max_length=100, required=False)
    duration = forms.CharField(max_length=100, required=False)

# Φόρμα για τιμητικές άδειες
class HonorLeaveForm(forms.Form):
    leave_type = forms.CharField(max_length=100, required=False)
    duration = forms.CharField(max_length=100, required=False)
