# -*- coding: utf-8 -*-
# models.py for images_engine

import datetime
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

#from django.contrib.auth.models import User

from imagekit.models import ImageModel


class Image(ImageModel):
    title = models.CharField(
        max_length=120,
        verbose_name='Название',
        help_text='название изображения',
        unique=True,)
    title_slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    original_image = models.ImageField(
        upload_to='uploads',
        verbose_name='image',
        help_text='картинка',)
    num_views = models.PositiveIntegerField(
        editable=False,
        default=0,)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'images_engine.specs'
        cache_dir = 'uploads/chache'
        image_field = 'original_image'
        save_count_as = 'num_views'


    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural= 'Картинки'

    def save(self, *args, **kwargs):
        self.datetime_modifed = datetime.datetime.now()
        if self.title_slug is None:
            self.title_slug = slugify(self.title)

        super(Image, self).save(*args, **kwargs)


#    @permalink
#    def get_absolute_url(self):
#        return ('name', None, {'name': self.name})


class Gallery(models.Model):
    name = models.CharField(
        max_length=120,
        verbose_name='Название альбома',
        help_text='название альбома',
        unique=True,)
    name_slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)


    images = models.ManyToManyField('Image',
        blank=True,
        null=True,
        verbose_name=u'Картинки',
        help_text=u'выберите одну или несколько картинок.')


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural= 'Галлереи'

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Gallery, self).save(*args, **kwargs)
