# -*- coding: utf-8 -*-
# models.py for pages_engine
# TODO: Приведение всех введенных пользователем данных(телефоны, icq и проч.)
# к единому виду

import datetime
from django.db import models
from django.db.models import permalink
from markdown import markdown
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, UserManager

from projectapps.imaginary.models import Image
from projectapps.accounter.page_widgets import *



#####   Адреса   |-----------------------------------------------------------------
class Address(models.Model):
    ADRES_TYPE_CHOICES = (
        ('UL', u'Улица'), ('PR', u'Проспект'), ('PL', u'Площадь'), ('PE', u'Переулок'), ('NA', u'Набережная'), ('AL', u'Аллея'),
        ('HW', u'Шоссе'), ('PZ', u'Проезд'), ('LI', u'Линия'), ('LU', u'Луч'), ('SP', u'Спуск'), ('SE', u'Съезд'),)
    descr_choices = {
        'UL':u'Улица', 'PR':u'Проспект', 'PL':u'Площадь', 'PE':u'Переулок', 'NA':u'Набережная',
        'AL':u'Аллея', 'HW':u'Шоссе', 'PZ':u'Проезд', 'LI':u'Линия', 'LU': u'Луч', 'SP': u'Спуск', 'SE': u'Съезд',}
    descr_choices_small = {
        'UL':u'улица', 'PR':u'проспект', 'PL':u'площадь', 'PE':u'переулок', 'NA':u'набережная',
        'AL':u'аллея', 'HW':u'шоссе', 'PZ':u'проезд', 'LI':u'линия', 'LU': u'луч', 'SP': u'спуск', 'SE': u'съезд',}
    ADRES_TYPE_CHOICES_SHORT = (
        ('UL', u'ул'), ('PR', u'просп'), ('PL', u'пл'), ('PE', u'пер'), ('NA', u'наб'), ('AL', u'аллея'),
        ('HW', u'шоссе'), ('PZ', u'проезд'), ('LI', u'линия'), ('LU', u'луч'), ('SP', u'спуск'), ('SE', u'съезд'),)

    item_index = models.IntegerField(
        max_length=6,
        blank=True, null=True,
        verbose_name='Индекс',
        help_text='индекс',)
    city = models.CharField(
        max_length=65,
        default='Санкт-Петербург',
        verbose_name='Город',
        help_text='город',)
    street_type = models.CharField(
        max_length=2, blank=True,
        default='UL',
        choices=ADRES_TYPE_CHOICES_SHORT,
#        choices=ADRES_TYPE_CHOICES,
        verbose_name='Тип улицы',
        help_text='тип улицы',)
    street_type_arrange = models.BooleanField(
        default=False,
        verbose_name='Место типа',
        help_text='где будет стоят тип улицы, до или после названия',)
    street_name = models.CharField(
        blank=True, null=True,
        default='',
        max_length=35,
        verbose_name='Название улицы',
        help_text='полное название',)
    house = models.CharField(
        max_length=40, blank=True, null=True,
        verbose_name='Дом',
        help_text='номер дома',)
    corpus = models.CharField(
        max_length=40,
        blank=True, null=True,
        verbose_name='Корпус/строение/литера',
        help_text='корпус / строение',)
    appartment = models.CharField(
        max_length=40,
        blank=True, null=True,
        verbose_name='Офис / Квартира',
        help_text='номер квартиры / офиса',
    )

    geocode_flag = models.BooleanField(
        default=False,
        verbose_name='Включить GeoCoder',
        help_text='использовать ли адрес для автоматического поиска',)
    location_manual_latitude = models.FloatField(
        editable=False, null=True, blank=True,)
    location_manual_longitude = models.FloatField(
        editable=False, null=True, blank=True,)
    location_auto = LocationField(
        max_length=255, blank=True,)

    def __unicode__ (self):
        return u'%s %s, г. %s' % (self.street_name, self.house, self.city,)

    class Meta:
#        abstract = True
        verbose_name = u'Адрес'
        verbose_name_plural= u'Адреса'


    def save(self, *args, **kwargs):
        if not self.geocode_flag:
            location2 = u'%s+%s+%s,+%s' % (self.street_name, self.descr_choices[self.street_type], self.house, self.city)
            self.location_manual_latitude, self.location_manual_longitude = get_lat_long(location2)
            self.location_auto = u'%s,%s' % (self.location_manual_latitude, self.location_manual_longitude)
        else:
            self.geocode_flag = False
            self.location_manual_latitude, self.location_manual_longitude = self.location_auto.split(',')

        super(Address, self).save(*args, **kwargs)




#####   CustomUser   |-----------------------------------------------------
# TODO: аватарки ?
# TODO: все должности?
class CustomUser(User):
    '''
        модель для кастомного пользователя
    '''
    datetime_birth = models.DateTimeField(
        null=True, blank=True,
#        default=datetime.datetime.now,
        verbose_name='Дата рождения',)
    phone_mobile = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name='мобильный телефон',
        help_text='мобильный телефон',)
    phone_mobile_status = models.BooleanField(
        editable=False, default=False)
    icq = models.CharField(max_length=20,
        null=True, blank=True,
        verbose_name='ICQ',
        help_text='номер ICQ',)
    skype = models.CharField(
        max_length=100, blank=True,
        verbose_name='Skype',
        help_text='адрес Skype',)

    activation_code = models.CharField(
        max_length=200, blank=True,
        verbose_name='код активации',
        help_text='код активации',)

    objects = UserManager()


#    def __unicode__(self):
#        return self.skype

    def get_exact_profile(self):
        return True


    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural= u'Пользователи'



class Company(models.Model):
    owner = models.ForeignKey(CustomUser)

    name = models.CharField(
        max_length=225,
        verbose_name='Название',
        help_text='название задачи',
        unique=True,)
    name_slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)
    logo = models.ForeignKey(Image,
        null=True, blank=True,)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modified = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    is_visible = models.BooleanField(
        default=True)
    is_active = models.BooleanField(
        default=True)

    workers = models.ManyToManyField(CustomUser,
         related_name='company_workers',
         null=True, blank=True,)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'

    def save(self, *args, **kwargs):
        self.datetime_modified = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)





class PhoneStatus(models.Model):
    user = models.ForeignKey(CustomUser)
    phone_num = models.CharField(max_length=20)
    phrase = models.CharField(max_length=4)
    sms_id = models.CharField(
        max_length=10, null=True, blank=True,)
    sms_status = models.CharField(
        max_length=150, null=True, blank=True,)


class IpBan(models.Model):
    ipaddress = models.IPAddressField()
    datetime = models.DateTimeField()
    count = models.PositiveSmallIntegerField()
