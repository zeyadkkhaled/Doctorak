from django import forms
from .models import User, Doctor

class DoctorRegisterForm(forms.ModelForm):
    # User fields
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    # Doctor fields
    f_name = forms.CharField(max_length=50)
    l_name = forms.CharField(max_length=50)
    gender = forms.CharField(max_length=10)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    speciality = forms.CharField(max_length=100)
    experience = forms.IntegerField()

    class Meta:
        model = Doctor
        fields = ['f_name', 'l_name', 'gender', 'dob', 'phone', 'address', 'speciality', 'experience']
