# -*- coding: utf-8 -*-
# models.py for imaginary

import datetime
from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from pytils.translit import slugify as slugify_p
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

#from django.contrib.auth.models import User

from imagekit.models import ImageModel


class Image(ImageModel):
    title = models.CharField(
        max_length=120,
        verbose_name='Название',
        help_text='название изображения',)
    title_slug = models.SlugField(
        max_length=150,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    datetime_created = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата внесения',)
    datetime_modifed = models.DateTimeField(
        default=datetime.datetime.now,
        verbose_name='Дата изменения',)

    def image_filename(instance, filename):
        fname, extension = filename.rsplit('.')
        slug = slugify_p(unicode(fname))
        return 'uploads/%s.%s' % (slug, extension) 

    original_image = models.ImageField(
        upload_to=image_filename,
        verbose_name='image',
        help_text='картинка',)
    num_views = models.PositiveIntegerField(
        editable=False,
        default=0,)

    gallery = models.ForeignKey('Gallery', blank=True, null=True,
        verbose_name='Галлерея', related_name='gallery')

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'imaginary.specs'
        cache_dir = 'images_e/images/chache'
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
    name = models.CharField(max_length=120,
        verbose_name='Название альбома',
        help_text='название альбома',)
    name_slug = models.SlugField(max_length=150,
        verbose_name='Короткое название',
        help_text='короткое название для URL, даётся автоматом, но можно изменять',)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Галлерея'
        verbose_name_plural= 'Галлереи'

    def save(self, *args, **kwargs):
        if self.name_slug is None:
            self.name_slug = slugify(self.name)

        super(Gallery, self).save(*args, **kwargs)


class GalleryRel(models.Model):
    gallery = models.ForeignKey(Gallery, verbose_name='Галерея')

    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class Galleried(models.Model):
    def get_gallery(self):
        item_type = ContentType.objects.get_for_model(self)
        try:
            gallery = GalleryRel.objects.get(content_type__pk=item_type.id,
                object_id=self.id)
            images = Image.objects.filter(gallery=gallery.gallery)
            return images
        except GalleryRel.DoesNotExist, Image.DoesNotExist:
            return None
    class Meta:
        abstract=True
