
from django.urls import path
from app.views import signUp, success, profile, deleteAcc, changeEmail, testingA, testingB
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .form import AllAuthenticationForm, PasswordChange, PasswordConfirm





urlpatterns = [

   path('testingA/', testingA.as_view(), name='testingA'),
   
   path('testingB/', testingB.as_view(), name='testingB'),
   
   path('accounts/signup/', signUp.as_view(), name='signup'),
   
   path('accounts/profile/', login_required(profile.as_view()), name='profileupdate'),
   
   path('accounts/delete', login_required(deleteAcc.as_view()), name='deleteacc'),
   
   path('success/', success.as_view(), name='success'),
   
   path('accounts/login/', auth_views.LoginView.as_view(template_name="loginForm.html", redirect_authenticated_user=True, authentication_form=AllAuthenticationForm), name="login"),
   
   path('accounts/logout/', login_required(auth_views.LogoutView.as_view(next_page='/accounts/login/'))),
   
   path('accounts/password_change/', login_required(auth_views.PasswordChangeView.as_view(template_name="password_change_form.html", success_url='/success/', form_class=PasswordChange)), name="password_change"),
   
   path('accounts/email_change/', login_required(changeEmail.as_view()), name="email_change"),
   
   path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html", success_url='/success/', html_email_template_name="password_reset_email.html"), name="password_reset"),
   
   path('accounts/password_reset_confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", success_url='/success/', form_class=PasswordConfirm), name="password_reset_confirm"),
   
]

