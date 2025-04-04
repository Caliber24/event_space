from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):
  
  def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_active', True)
    return self.create_user(email=email, password=password, **extra_fields)
  def create_user(self, email,password=None, **extra_fields):
    if not email:
      raise ValueError('The Email field must be set.')
    extra_fields.setdefault('is_active', True)
    email= self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

class User(AbstractUser):
  first_name = models.CharField(max_length=255, null=True, blank=True)
  last_name = models.CharField(max_length=255, null=True, blank=True)
  username = models.CharField(max_length=255, null=True, blank=True)
  email =models.EmailField(unique=True)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS=[]
  
  objects = CustomUserManager()
  
  def __str__(self):
    return self.email