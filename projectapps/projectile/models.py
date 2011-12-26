# -*- coding: utf-8 -*-
# models.py for pages_engine

import datetime
#from django.db import models
from django.db import models as m
from django.db.models import permalink

from markdown import markdown
from django.template.defaultfilters import slugify


from django.contrib.auth.models import User

try:
    from pytils.translit import slugify
except ImportError:
    from django.template.defaultfilters import slugify
from p_utils import lang_stub as _
#from django.utils.translation import ugettext_lazy as _

from commonapps.treebeard.mp_tree import MP_Node
from projectapps.accounter.models import CustomUser
from admin_tools.dashboard import modules




class Project(m.Model):

    name = m.CharField(max_length=225, verbose_name='Название',
                            help_text='название компонента',)
    name_slug = m.SlugField(max_length=250, verbose_name='Короткое название',
                                 help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    description_markdown = m.TextField(null=True, blank=True, verbose_name='Короткое описание',
                                            help_text='короткое описание',)
    description_html = m.TextField(editable=False,)

    datetime_created = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата внесения',)
    datetime_modifed = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения',)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name, verbose_name_plural = ('Проект', 'Проекты')


    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description_markdown)
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Project, self).save(*args, **kwargs)


class Component(m.Model):

    name = m.CharField(max_length=225, unique=True, verbose_name='Название',
                            help_text='название компонента',)
    name_slug = m.SlugField(max_length=250, unique=True, verbose_name='Короткое название',
                                 help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    description_markdown = m.TextField(null=True, blank=True, verbose_name='Короткое описание',)
    description_html = m.TextField(editable=False,)
    datetime_created = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата внесения',)
    datetime_modifed = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения',)

    project = m.ForeignKey(Project)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural= 'Компоненты'


    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description_markdown)
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Component, self).save(*args, **kwargs)



# TODO: сделать необязательное поле для времени релиза
class Milestone(m.Model):

    TYPES_CHOICES = (('RE', u'Релиз'), ('MS', u'Веха'),)

    name = m.CharField(max_length=225, verbose_name='Название',
                            help_text='название компонента',)
    name_slug = m.SlugField(max_length=250, verbose_name='Короткое название',
                                 help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    type = m.CharField(max_length=2, choices=TYPES_CHOICES)
    description_markdown = m.TextField(null=True, blank=True, verbose_name='Короткое описание',
                                            help_text='короткое описание',)
    description_html = m.TextField(editable=False,)

    datetime_created = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата внесения',)
    datetime_modifed = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения',)
    datetime_release = m.DateTimeField(verbose_name='Дата выпуска',)

    project = m.ForeignKey(Project)


    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name, verbose_name_plural = ('Выпуск', 'Выпуски')
        unique_together = (('name', 'project'), ('name_slug', 'project'),)


    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description_markdown)
        self.datetime_modifed = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Milestone, self).save(*args, **kwargs)





class Task(MP_Node):

    TYPES_CHOICES = (('BUG', u'Баг'), ('ENC', u'Улучшение'), ('TAS', u'Задача'),)
    PRIORITIES_CHOICES = (('BLK', u'Блокирующе'), ('CRT', u'Критично'), ('MAJ', u'Важно'), ('NRM', u'Средне'),
        ('MDL', u'Слабое'), ('LOW', u'Низкое'))

    STATUS_CHOICES = (('WIT', 'waiting'), ('HLD', 'on hold'), ('WIP', 'in progress'), ('DNE', 'done'),
        ('CFD', 'confirmed'), ('CLD', 'closed'),)
    STATUS_CHOICES_RU = (('WIT', 'wait'), ('HLD', 'on hold'), ('WIP', 'in progress'), ('DNE', 'done'),
        ('CFD', 'confirmed'), ('CLD', 'closed'),)

    name = m.CharField(max_length=225, unique=True, verbose_name='Название',
                            help_text='название компонента',)
    name_slug = m.SlugField(max_length=250, unique=True, verbose_name='Короткое название',
                                 help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    type = m.CharField(max_length=3, choices=TYPES_CHOICES)
    priority = m.CharField(max_length=3, choices=PRIORITIES_CHOICES)
    status = m.CharField(max_length=3, choices=STATUS_CHOICES)

    time_required_str = m.CharField(null=True, blank=True, max_length=225)
    time_required_int = m.PositiveSmallIntegerField(null=True, blank=True, editable=False,)
    time_final_str = m.CharField(null=True, blank=True, max_length=225, editable=False)
    time_final_int = m.PositiveSmallIntegerField(null=True, blank=True, editable=False,)

    description_markdown = m.TextField(null=True, blank=True, verbose_name='Короткое описание',
                                            help_text='короткое описание',)
    description_html = m.TextField(editable=False,)

    datetime_created = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата внесения',)
    datetime_modifed = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения',)
    datetime_end = m.DateTimeField(default=datetime.datetime.now, verbose_name='Дата окончания',)

    user_author = m.ForeignKey(User, related_name='user_author')
    user_executive = m.ForeignKey(User, related_name='user_executive', null=True, blank=True,)

    project = m.ForeignKey(Project)
    component = m.ForeignKey(Component, null=True, blank=True,)
    release  = m.ForeignKey(Milestone, null=True, blank=True,)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = ('Task', 'Tasks')

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description_markdown)
        self.datetime_modified = datetime.datetime.now()
        if self.name_slug is None:
            self.name_slug = slugify(self.name)
        super(Task, self).save(*args, **kwargs)




class TaskStates(m.Model):

    description_markdown = m.TextField(null=True, blank=True, verbose_name='Короткое описание',
                                            help_text='короткое описание',)
    description_html = m.TextField(editable=False,)

#    task_id = m.PositiveIntegerField()
    task_id = m.ForeignKey(Task,)
    user_author = m.ForeignKey(User,)


#    def __unicode__(self):
#        return self.name

    class Meta:
        verbose_name, verbose_name_plural = ('Task state', 'Task states')

    def save(self, *args, **kwargs):
        self.description_html = markdown(self.description_markdown)
        self.datetime_modified = datetime.datetime.now()
        super(TaskStates, self).save(*args, **kwargs)