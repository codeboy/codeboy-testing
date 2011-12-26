# -*- coding: utf-8 -*-
# forms.py for accounter
import datetime
from django import forms
from django.forms import ModelForm
from models import CustomUser, Address
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, Textarea, PasswordInput, EmailField, CheckboxInput
from django.forms.extras.widgets import SelectDateWidget

from projectapps.imaginary.models import Image


class AdressForm(ModelForm):
    city = forms.CharField(label='Город', required=True)
    street_name = forms.CharField(label='Улица', required=True)
    house = forms.CharField(label='Дом', required=True)
    class Meta:
        model = Address
        exclude = ('geocode_flag', 'street_type_arrange', 'location_auto')


class CustomUserForm(ModelForm):
    email = EmailField(label='E-mail')
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    class Meta:
        model = CustomUser
        exclude = ('username', 'password', 'is_staff', 'is_active',
            'is_superuser', 'last_login', 'date_joined', 'groups',
            'user_permissions', 'image', 'activation_code')
        widgets = {
            'datetime_birth': SelectDateWidget(years=range(1930,datetime.date.today().year))}


class ImageForm(ModelForm):
    class Meta:
        model = Image
#        fields = ('original_image')


class RegistrationForm(ModelForm):
    password2 = forms.CharField(label='Повторите пароль', widget=PasswordInput)
    email = EmailField(label='E-mail')
    phone_main = forms.CharField(label='Контактный телефон', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Введенные пароли не совпадают.")
        return password2


    class Meta:
        model = CustomUser
        exclude = ('is_staff', 'is_active', 'is_superuser', 'last_login',
            'date_joined', 'groups', 'user_permissions')
#        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password' : PasswordInput,
            'datetime_birth': SelectDateWidget(years=range(1930,datetime.date.today().year))}




class PasswordResetRequestForm(forms.Form):
    '''
    форма к запросу пароля
    '''
#    email = forms.EmailField(label='E-mail', required=True)
    login = forms.CharField(label='Login', required=True)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=(u"Новый пароль"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=(u"Пароль ещё раз"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError((u"Оба пароля должны совпадать."))
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


