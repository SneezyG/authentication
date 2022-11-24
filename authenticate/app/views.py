from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from .models import User
from .form import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse


# Create your views here.

  
  
  
  
class signUp(View):

  """
  this view return a signup page on get request, register a user on post request.
  """
  
  form_class = UserForm
  initial = {'key': 'value'}
  template = 'createForm.html'
  success = 'success.html'
  
  
  def get(self, request, *args, **kwargs):
    form = self.form_class(initial= self.initial)
    return render(request, self.template, {'form': form})
    
  
  def post(self, request, *args, **kwargs):
   
     form = self.form_class(request.POST)
     email = request.POST['email']
     password = request.POST['password']
     username = request.POST['username']
     
     if form.is_valid():
        User.objects.create_user(username, email, password)
        user = authenticate(request, email=email, password=password)
        login(request, user)
        
        return HttpResponseRedirect('/success/')
       
     return render(request, self.template, {'form': form})
       
     


 
 
class success(View):
  
  """
  this return the success page.
  """
  
  template = 'success.html'
  
  def get(self, request, *args, **kwargs):
   
      url = request.headers['REFERER']
      pk = request.user.id
      items = url.rsplit('/')
      referrer = items[-2]
        
      if referrer == "password_change":
        logout(request)
        text = "your password have been change successfully."
        
      elif referrer == "signup":
        text = "your account have been created successfully and your account logged in."
       
      else:
        text = "Profile updated successfully."
        
      messages.info(request, text)
      return render(request, self.template, {'pk':pk})
  



class logIn(View):
  """
  this view authenticate and log the user in.
  """
  
  form_class = AuthenticationForm
  initial = {'key': 'value'}
  template = 'loginForm.html'
  
  def get(self, request, *args, **kwargs):
    if request.user.id:
      return HttpResponseRedirect(reverse('app:profileupdate', args=(request.user.id,)))
    form = self.form_class(initial= self.initial)
    return render(request, self.template, {'form': form})

  def post(self, request, *args, **kwargs):
    form = self.form_class(request, request.POST)
    email = request.POST['username']
    password = request.POST['password']
    
    if form.is_valid():
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('app:profileupdate', args=(user.id,)))
        
        
    return render(request, self.template, {'form': form})
       
  
  

class profile(UpdateView):
  
  """
  this view display and update the user profile.
  """
  
  model = User
  fields = ["username", "first_name", "last_name", "avatar"]
  template_name = "profile.html"
  success_url = '/success/'
 
  

    
    


class deleteAcc(TemplateView):
  
  """
  this view log a user out and deactivate the user account.
  """
  template_name = 'delete_acc.html'
  
  def get(self, request, *args, **kwargs):
    pk = request.user.id
    User.objects.get(pk=pk).delete()
    logout(request)
    return super().get(request, *args, **kwargs)
  
 
 
  
