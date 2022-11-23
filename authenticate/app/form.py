import re
from django.forms import ModelForm
from .models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm





"""
custom validator for my extended PasswordChangeForm and SetPasswordForm
"""
def custom_validator(value):
  text = "password must contain a letter, number and at least 9 characters"
  
  if len(value) < 9:
    raise ValidationError(text)
    
  find_number = re.search("[0-9]", value)
  if not find_number: 
    raise ValidationError(text)
  
  find_letter = re.search("[a-zA-Z]", value)  
  if not find_letter:
    raise ValidationError(text)
  





class PasswordChange(PasswordChangeForm):
  
  """
  this form class extend build in PasswordChangeForm with a customized password validator.
  """
 
  new_password1 = forms.CharField(widget=forms.PasswordInput, label="New password", validators=[custom_validator,])
  
  new_password2 = forms.CharField(widget=forms.PasswordInput, label="New password confirmation", validators=[custom_validator,])
  
  
  




class UserForm(ModelForm):
  
  """
  this form class generate the form inputs for user signup
  """
  password = forms.CharField(widget=forms.PasswordInput, help_text="password must contain a letter, number and at least 9 characters", validators=[custom_validator,])
  
  class Meta:
    model = User
    fields = ['username', 'email',]
 
 
 
 
 
    

    
  
  
  
    
    