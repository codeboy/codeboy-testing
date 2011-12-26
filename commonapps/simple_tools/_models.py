# -*- coding: utf-8 -*-

import datetime
from django.db import models

# импорт виджета для карт
from widgets import *
# markdown собствено
from markdown import markdown

#from photologue.models import ImageModel
#from photologue.models import Photo

# для сейва slug
from django.template.defaultfilters import slugify

# сигналы для пресейва
from django.db.models import signals

from django.contrib.auth.models import User

import mptt



class Post(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        help_text='название записи',
        unique=True,)
    name_slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    descripttion_markdown = models.TextField(
        null=False,
        blank=False,
        verbose_name='Короткое описание',
        help_text='короткое описание',)
    descripttion_html = models.TextField(
        editable=False,)

    content_markdown = models.TextField(
        null=False,
        blank=True,
        verbose_name='Основной текст',
        help_text='основной текст',)
    content_html = models.TextField(
        editable=False,)

    categories = models.ManyToManyField('Category',
        blank=True,
        null=True,
        verbose_name=u'Категории',
        help_text=u'выберите одну или несколько категорий.',)

    tags = models.ManyToManyField('Tag',
        blank=True,
        null=True,
        verbose_name=u'Метки',
        help_text=u'выберите одну или несколько меток.',)

    user = models.ForeignKey(User,
        null=False,
        blank=True,
        verbose_name=u'Автор',
        help_text=u'выберите автора.',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural= 'Записи'

    def save(self, *args, **kwargs):
        self.descripttion_html = markdown(self.descripttion_markdown)
        self.content_html = markdown(self.content_markdown)

        self.datetime_modifed = datetime.datetime.now()

        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Post, self).save(*args, **kwargs)





class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='имя категории',
        unique=True,)
    name_slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    descripttion_markdown = models.TextField(
        null=False,
        blank=False,
        verbose_name='Короткое описание',
        help_text='короткое описание',)
    descripttion_html = models.TextField(
        editable=False,)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural= 'Категории'

    def save(self, *args, **kwargs):
        self.descripttion_html = markdown(self.descripttion_markdown)

        self.datetime_modifed = datetime.datetime.now()

        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)



class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя метки',
        unique=True,)
    name_slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    descripttion_markdown = models.TextField(
        null=False,
        blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)
    descripttion_html = models.TextField(
        editable=False,)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural= 'Метки'

    def save(self, *args, **kwargs):
        self.descripttion_html = markdown(self.descripttion_markdown)

        self.datetime_modifed = datetime.datetime.now()

        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Pages, self).save(*args, **kwargs)




class Pages(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        help_text='название страницы',
        unique=True,)
    name_slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    descripttion_markdown = models.TextField(
        null=False,
        blank=True,
        verbose_name='Короткое описание',
        help_text='короткое описание',)
    descripttion_html = models.TextField(
        editable=False,)

    content_markdown = models.TextField(
        null=False,
        blank=True,
        verbose_name='Основной текст',
        help_text='основной текст',)
    content_html = models.TextField(
        editable=False,)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural= 'Страницы'

    def save(self, *args, **kwargs):
        self.descripttion_html = markdown(self.descripttion_markdown)
        self.content_html = markdown(self.content_markdown)

        self.datetime_modifed = datetime.datetime.now()

        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Pages, self).save(*args, **kwargs)


#try:
#    mptt.register(Pages, order_insertion_by=['name_slug'])
#except mptt.AlreadyRegistered:
#    pass



