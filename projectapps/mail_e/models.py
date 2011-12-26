# -*- coding: utf-8 -*-
from string import split
import datetime
from time import sleep
import smtplib
from django.db import models
from ckeditor.fields import RichTextField
from projectapps.accounter.models import Address, CustomUser
from projectapps.catalog_engine.models import Brand
from projectapps.tags_e.models import Tag
from p_utils import send_sms as p_sms
from utils import send_mail3 as dj_send_mail
from p_utils import phone_formater

STATUS_CHOICES = (('BGN', u'In the beginning'), ('STR', u'Started'),
                  ('PRO', u' In process'), ('ERR', u'Error'),
                  ('ERD', u'Done with errors'), ('SNT', u'Sent'))



class Mailer(models.Model):
    start = models.DateTimeField(null=True, blank=True,
        verbose_name="Дата начала")
    end = models.DateTimeField(null=True, blank=True,
        verbose_name="Дата окончания")
    count = models.IntegerField(null=True, blank=True,
        verbose_name="Количество отправленных писем")
    subject = models.CharField(max_length=225, null=True, blank=False,
        verbose_name="Тема письма")
    body = RichTextField(null=True, blank=False,
        verbose_name="Содержание письма")
    filters = models.ForeignKey('Filter', null=True, blank=True,
        verbose_name="Фильтры")
    users = models.ManyToManyField(CustomUser, through='MailerUsers',
        null=True, blank=True, verbose_name="Выборка пользователей")
    status = models.CharField('Статус', null=True, blank=True,
        choices=STATUS_CHOICES, default='BGN', max_length=3)
    counter = models.IntegerField('Сообщений отправлено', null=True, blank=True,
        default=0)
    all_users = models.BooleanField('Все пользователи', default=False)
    sms = models.BooleanField('СМС', default=False, help_text='Отметьте здесь,\
        если хотите сделать смс-рассылку')

    def get_recipients(self):
        emails = []
        users = MailerUsers.objects.filter(mailer=self)
        for user in users:
            if user.mail:
                emails.append(user.mail)
        return emails

    def _add_all_users(self):
        users = CustomUser.objects.filter(subscription_av=True,
                                          subscription_offer=True,
                                          subscription_sales=True)
        for user in users:
            u, created = MailerUsers.objects.get_or_create(user=user, mailer=self,)
            u.status = 'PRO'
            u.save()
        return

    def _add_recipients_by_city(self):
        cities = split(self.filters.cities, ', ')
        if not cities[-1]:
            cities = cities[:-1]
        users = CustomUser.objects.filter(company__address_real__city__in=cities,
                                           subscription_offer=True,
                                           subscription_av=True,
                                           subscription_sales=True,)
        for user in users:
            u, created = MailerUsers.objects.get_or_create(user=user, mailer=self)
            u.status = 'PRO'
            u.save()
        return

    def _add_recipients_by_tag(self):
        tags = self.filters.tags.all()
        for tag in tags:
            users = CustomUser.objects.filter(tag=tag,
                                              subscription_offer=True,
                                              subscription_av=True,
                                              subscription_sales=True,)
            for user in users:
                u, created = MailerUsers.objects.get_or_create(user=user, mailer=self)
                u.status = 'PRO'
                u.save()
        return

    def _add_recipients(self):
        if self.all_users:
            self._add_all_users()
        else:
            self._add_recipients_by_city()
            self._add_recipients_by_tag()
        if self.sms:
            users = MailerUsers.objects.filter(mailer=self,
                user__phone_mobile_status=False)
            for user in users:
                user.delete()
        return

    def send_mail(self):
        self.status = 'PRO'
        self.save()
        users = MailerUsers.objects.filter(mailer=self)
        self.counter = 0

        for user in users:
            if dj_send_mail([user.mail,], self.subject, self.body,) != 0:
                user.sent_at = datetime.datetime.now()
                user.status = 'SNT'
                self.counter += 1
            else:
                user.status = 'ERR'
                self.status = 'ERR'
            user.save()
            self.save()

        if self.status != 'ERR':
            self.status = 'SNT'
        else:
            self.status = 'ERD'
        self.save()
        return

    def send_sms(self):
        self.status = 'PRO'
        self.save()
        users = MailerUsers.objects.select_related().filter(mailer=self)
        self.counter = 0

        for user in users:
            sms_result = p_sms('+7%s' % phone_formater(user.user.phone_mobile), str(self.body))
            sms_id, sms_status = sms_result.split('=')

            if sms_status == 'accepted':
                user.status = 'SNT'
                user.sent_at = datetime.datetime.now()
            else:
                user.status = 'ERR'
                self.status = 'ERR'
            user.save()
            self.save()

        if self.status != 'ERR':
            self.status = 'SNT'
        else:
            self.status = 'ERD'
        self.save()
        return

    def send(self):
        if self.sms:
            self.send_sms()
        else:
            self.send_mail()

    def save(self, commit=True, *args, **kwargs):
        if self.status == 'STR':
            self.start = datetime.datetime.now()
        elif self.status == 'SNT' or self.status == 'ERD':
            self.end = datetime.datetime.now()
        super(Mailer, self).save(*args, **kwargs)
        if commit and not self.users.all():
            self._add_recipients()

    def __unicode__(self):
        return self.subject


class MailerUsers(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь")
    mailer = models.ForeignKey('Mailer', verbose_name="Рассылка")
    mail = models.CharField(max_length=225, verbose_name="E-mail пользователя")
    sent_at = models.DateTimeField(null=True, blank=True,
        verbose_name="Время отправления")
    status = models.CharField(max_length=3, choices=STATUS_CHOICES,
        verbose_name="Состояние рассылки")
    def save(self, *args, **kwargs):
        self.mail = self.user.email
        super(MailerUsers, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.user.username


class Filter(models.Model):
    tags = models.ManyToManyField(Tag, related_name="filter_tag",
        verbose_name="Теги", null=True, blank=True)
    cities = models.CharField(max_length=225, verbose_name="Города", null=True,
        blank=True, help_text='введите названия городов,\
        перечисленные через запятую(и пробел)')
