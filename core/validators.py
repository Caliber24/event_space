from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import exceptions

def check_user_found(email):
  return get_object_or_404(get_user_model(), email=email)
    
def check_user_password(email, password):
  user = check_user_found(email)
  if not user.check_password(password):
    raise exceptions.AuthenticationFailed('Password is incorrect')