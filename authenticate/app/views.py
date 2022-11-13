from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from .models import User
from .form import UserForm
from django.http import HttpResponse, HttpResponseRedirect
from verify_email.email_handler import send_verification_email
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.




class testingA(TemplateView):
  template_name = "password_reset_email.html"
  

class testingB(View):
  form_class = UserForm
  initial = {'key': 'value'} 
  template = 'password_reset_email.html'
  
  def get(self, request, *args, **kwargs):
    #raise notfound
    form = self.form_class(initial= self.initial)
    return render(request, self.template, {'form': form})
  
  
  
  
class signUp(View):

  """
  this view return a signup page on get request, register a user on post request and send a verification link.
  """
  
  form_class = UserForm
  initial = {'key': 'value'}
  template = 'createForm.html'
  success = 'success.html'
  
  
  def get(self, request, *args, **kwarargs):
    form = self.form_class(initial= self.initial)
    return render(request, self.template, {'form': form})
    
  
  def post(self, request, *args, **kwargs):
   
     form = self.form_class(request.POST)
     email = request.POST['email']
     password = request.POST['password']
     
     if form.is_valid():
        inactive_user = send_verification_email(request, form)
       
        user = authenticate(request, email=email, password=password)
        login(request, user)
        
        text = "your account have been created, and account activation link have been sent to your email."
        
        messages.info(request, text)
        return render(request, self.success)
          
       
     return render(request, self.template, {'form': form})
       
     


 
 
class success(TemplateView):
  
  """
  this return the success page.
  """
  
  template_name = 'success.html'
  
  def get(self, request, *args, **kwargs):
    try:
      url = request.headers['REFERER']
      items = url.rsplit('/')
      referrer = items[-2]
      
      if referrer == "update_profile":
        text = "Profile updated successfully."
        
      elif referrer == "password_change":
        logout(request)
        text = "your password have been change successfully."
        
      elif referrer == "password_reset":
        text = "link to change your password have been sent to your email."
        
      else:
        raise KeyError()
        
    except:
      text = "your password have been reset successfully."
      
    messages.info(request, text)
    return super().get(request, *args, **kwargs)
  


class profile(UpdateView):
  
  """
  this view update the user profile.
  """
  
  model = User
  fields = ["username", "first_name", "last_name", "avater", "phone"]
  template_name = "profile.html"
  success_url = '/success/'
  
  def get(self, request, *args, **kwargs):
    self.object = request.user
    return super().get(request, *args, **kwargs)
    
  def get_object(self):
    return self.object
    
    


class deleteAcc(TemplateView):
  
  """
  this view log a user out and delete the account.
  """
  template_name = 'delete_acc.html'
  
  def get(self, request, *args, **kwargs):
    user = request.user
    user.set_unusable_password()
    user.save()
    logout(request)
    return super().get(request, *args, **kwargs)
  
 
 
  
