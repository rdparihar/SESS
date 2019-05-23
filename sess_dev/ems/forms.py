from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django import forms
from django.forms import ModelForm
from .models import EmpProfile
# from .models import Employee

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'date_joined']
        # username.help_text = ''
        labels = {
           'is_staff': "Staff privilege",
        }
        # username.help_text = ''
        # fields['username'].help_text = None
        widgets = {
            'username': forms.TextInput(attrs={ 'class': "form-control "}),
            'first_name' : forms.TextInput(attrs={ 'class': "form-control "}),
            'last_name' : forms.TextInput(attrs={'class': "form-control  "}),
            'email' : forms.TextInput(attrs={'type' : 'email','class': "form-control "}),
            'password' : forms.TextInput(attrs={'type' : 'password','class': "form-control "}),
            'is_staff' : forms.CheckboxInput(attrs={'class': "checkbox "}),
            'date_joined' : forms.TextInput(attrs={'type' : 'date','class': "form-control "})  
        }
        help_texts = {
            'username': _(''),
            'is_staff': _(''),
            'is_active': _(' '), 
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = EmpProfile
        fields = ['emp_dob', 'emp_doj', 'emp_con_primary', 'emp_con_secondary', 'emp_designation', 'emp_department']
        #fields = '__all__'
        # username.help_text = ''
        labels = {
          # 'is_staff': "Staff privilege",
        }
        # username.help_text = ''
        # fields['username'].help_text = None
        widgets = {
            'emp_dob': forms.DateInput(attrs={ 'class': "form-control input-rounded"}),
            'emp_doj' : forms.DateInput(attrs={'class': "form-control input-rounded "}),
            'emp_con_primary' : forms.TextInput(attrs={'class': "form-control input-rounded "}),
            'emp_con_secondary' : forms.TextInput(attrs={'class': "form-control  input-rounded"}),
            'emp_department' : forms.TextInput(attrs={'class': "form-control input-rounded"}),
            'emp_designation' : forms.TextInput(attrs={'class': "form-control input-rounded "})        
        }
        help_texts = {
            'emp_dob': _(''),
            'first_name': _(''),
            'emp_doj': _(' '),
            
        }