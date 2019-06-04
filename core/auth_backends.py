from core.models import User
from allauth.account.models import EmailAddress


class EmailAuthenticationBackend(object):
    """
    Authenticate users with 'Email'. Default implementation by django is 'username' and 'password'
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.filter(email=username)
            user = user.filter(is_active=True).get()
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            try:
                user = EmailAddress.objects.filter(email=username, verified=True).get().user
                if user.check_password(password):
                    return user
            except Exception:
                return None
        except User.MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
