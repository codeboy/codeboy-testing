# -*- coding: utf-8 -*-
# admin.py for accounter

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from django.utils.translation import ugettext, ugettext_lazy as _

from models import CustomUser, Address
from admin_forms import UserChangeForm


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'is_staff', 'is_active', 'skype', 'email',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Custom info'), {'fields': ('skype', 'icq', 'datetime_birth', 'phone_mobile',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    form = UserChangeForm
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)
    save_on_top = True
#admin.autodiscover()
#admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)


class AddressAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Address, AddressAdmin)



