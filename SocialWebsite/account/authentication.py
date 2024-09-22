# Making a custom authentication backend
# Packes
import email
from django.contrib.auth.models import User

class EmailAuthBackend(object):
    """
    Authenticate using an a-email address

    Args:
        object (_type_): object
    """
    def authenticate(self,request:str,username=None,password=None) -> object:
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user 
            return None
        except User.DoesNotExist:
            return None
    
    def get_user(self,user_id:int) -> object: # es usado para la duracion de la sesion de usuario
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None