from django import forms
from django.contrib.auth.forms import UserCreationForm
from my_work.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _



class PhoneNumberForm(forms.Form):
    mobile = forms.CharField(max_length=15, required=True)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class UserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=["username","full_name","password","email","user_type"]


class StudentForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["full_name","qualification","mobile","mail","course","subject"]


class TeacherForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["full_name","current_job","mobile","mail","adhar","training_sub"]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ClassForm1(forms.ModelForm):
    class Meta:
        model = ClassModel
        fields = ["subject", "classes", "time_slot", "price"]


class ClassForm2(forms.ModelForm):
    class Meta:
        model = ClassModel
        fields = ["discout", "offer", "emi"]


