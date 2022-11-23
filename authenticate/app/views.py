from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from .models import User
from .form import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

  
  
  
  
class signUp(View):

  """
  this view return a signup page on get request, register a user on post request.
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
     username = request.POST['username']
     
     if form.is_valid():
        User.objects.create_user(username, email, password)
        user = authenticate(request, email=email, password=password)
        login(request, user)
        
        text = "your account have been created successfully and your account logged in"
        
        messages.info(request, text)
        return render(request, self.success)
          
       
     return render(request, self.template, {'form': form})
       
     


 
 
class success(TemplateView):
  
  """
  this return the success page.
  """
  
  template_name = 'success.html'
  
  def get(self, request, *args, **kwargs):
   
      url = request.headers['REFERER']
      items = url.rsplit('/')
      referrer = items[-2]
      
      if referrer == "update_profile":
        text = "Profile updated successfully."
        
      else referrer == "password_change":
        logout(request)
        text = "your password have been change successfully."
        
      messages.info(request, text)
      return super().get(request, *args, **kwargs)
  


class profile(UpdateView):
  
  """
  this view display and update the user profile.
  """
  
  model = User
  fields = ["username", "first_name", "last_name", "avatar"]
  template_name = "profile.html"
  success_url = '/success/'
  
  def get(self, request, *args, **kwargs):
    self.object = request.user
    return super().get(request, *args, **kwargs)
    
  def get_object(self):
    return self.object
    
    


class deleteAcc(TemplateView):
  
  """
  this view log a user out and deactivate the user account.
  """
  template_name = 'delete_acc.html'
  
  def get(self, request, *args, **kwargs):
    user = request.user
    user.set_unusable_password()
    user.save()
    logout(request)
    return super().get(request, *args, **kwargs)
  
 
 
  
