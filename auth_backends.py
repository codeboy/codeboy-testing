# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, check_password
from django.db.models import get_model
from django.core.exceptions import ImproperlyConfigured
from projectapps.accounts_engine.models import CustomUser



class CustomUserModelBackend(ModelBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """
#    def authenticate(self, username=None, password=None):
#        login_valid = (settings.ADMIN_LOGIN == username)
#        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#        if login_valid and pwd_valid:
#            try:
#                user = User.objects.get(username=username)
#            except User.DoesNotExist:
#                Create a new user. Note that we can set password
#                to anything, because it won't be checked; the password
#                from settings.py will.
#                user = User(username=username, password='get from settings.py')
#                user.is_staff = True
#                user.is_superuser = True
#                user.save()
#            return user
#        return None

#    def get_user(self, user_id):
#        try:
#            return User.objects.get(pk=user_id)
#        except User.DoesNotExist:
#            return None



    def authenticate(self, username=None, password=None):
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None


    def get_mail(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None


    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class


