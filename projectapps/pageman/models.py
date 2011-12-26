# -*- coding: utf-8 -*-
# models.py for pageman

import datetime
from django.db import models as m
from django.db.models import permalink

try:
    from pytils.translit import slugify
except ImportError:
    from django.template.defaultfilters import slugify
from p_utils import lang_stub as _
#from django.utils.translation import ugettext_lazy as _

from commonapps.treebeard.mp_tree import MP_Node

from admin_tools.dashboard import modules

class Page(MP_Node):
    name = m.CharField(
        max_length=220,
        help_text=_('this is name'),)
    name_slug = m.CharField(
        max_length=220,
        help_text=_('this is slug name'),)

    teaser = m.TextField(
        blank=True,
        help_text=_('this is short teaser'),)
    body = m.TextField(
        help_text=_('this is main text'),)

    datetime_created = m.DateTimeField(
        default=datetime.datetime.now,
        verbose_name=_('time created'),)
    datetime_modifed = m.DateTimeField(
        default=datetime.datetime.now,
        editable=False,
        verbose_name=_('time changed'),)


    def save(self, *args, **kwargs):
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Page, self).save(*args, **kwargs)


class Article(m.Model):
    pass
