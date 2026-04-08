from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import ServiceRecord, UnderServiceRecord

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)

class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['bike_model', 'owner_name', 'contact', 'last_serviced_date', 'reg_no']

# ✅ Correct model used here
class UnderServiceForm(forms.ModelForm):
    class Meta:
        model = UnderServiceRecord
        fields = ['service_record', 'issue_description', 'progress']
