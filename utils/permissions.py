from rest_framework.permissions import BasePermission

class IsOwner(BasePermission) :
  def has_permission(self, request, view):
    if request.user.is_authenticated:
      if request.user.email == view.kwargs.get('email'):
        return True
    return False