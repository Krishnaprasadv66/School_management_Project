from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()  # This ensures the custom user model is used
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None