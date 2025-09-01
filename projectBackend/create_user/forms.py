from django import forms
from .models import Doctor, Patient, Visit

# from doctor table
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['national_id', 'username', 'password', 'email', 'specialist']
        widgets = {
            'password': forms.PasswordInput(),  # hide password input
        }

#from pAtient
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['national_id', 'full_name', 'dob', 'gender', 'blood_group', 'height', 'weight', 'mobile_number', 'allergies']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }

# forms.py


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['patient', 'doctor', 'hospital', 'notes']