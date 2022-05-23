import string
from django.utils.crypto import get_random_string

VALID_KEY_CHARS = string.ascii_lowercase + string.digits

class SessionBase:
    def get_new_session_key(self):
        while True:
            session_key = get_random_string(32, VALID_KEY_CHARS)
            if not self.filter(key=session_key).exists():
                return session_key

    def do_login(self, login, password):
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return None
        if user.password != password:
            return None
        self = Session()
        value = str(login) + str(password)
        self.key = value
        self.user = user
        self.expires = timezone.now() + timedelta(days=1)
        try:
            old_session=Session.objects.get(user=user) #expires__lt=timezone.now())
            old_session.delete()
        except self.DoesNotExist:
            pass
        self.save()
        return self