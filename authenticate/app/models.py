
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


def path(instance, filename):
  return 'avatar/user_{0}/{1}'.format(instance.id, filename)


class User(AbstractUser):
  
  """
  store a single user data.
  inherit the django abstract user class.
  and this model is the new auth_user_model
  """
  
  username = models.CharField(max_length=30, unique=False)
  email = models.EmailField(unique=True)
  avatar = models.ImageField(upload_to=path, null=True, blank=True)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']
  
  def __str__(self):
     return self.email
     