
from django.urls import path
from app.views import signUp, success, profile, deleteAcc, changeEmail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .form import PasswordChange





urlpatterns = [
   
   path('accounts/signup/', signUp.as_view(), name='signup'),
   
   path('accounts/profile/', login_required(profile.as_view()), name='profileupdate'),
   
   path('accounts/delete', login_required(deleteAcc.as_view()), name='deleteacc'),
   
   path('success/', success.as_view(), name='success'),
   
   path('accounts/login/', auth_views.LoginView.as_view(template_name="loginForm.html", redirect_authenticated_user=True), name="login"),
   
   path('accounts/logout/', login_required(auth_views.LogoutView.as_view(next_page='/accounts/login/')), name="logout"),
   
   path('accounts/password_change/', login_required(auth_views.PasswordChangeView.as_view(template_name="password_change_form.html", success_url='/success/', form_class=PasswordChange)), name="password_change"),
   
]

