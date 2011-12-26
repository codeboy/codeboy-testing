# -*- coding: utf-8 -*-
# admin.py for images_engine

from django.contrib import admin
from models import Image, Gallery


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime_created', 'admin_thumbnail_view')
    list_filter = ['datetime_created', 'title']
    list_per_page = 25

    prepopulated_fields = {"title_slug": ("title",)}
    save_on_top = True
admin.site.register(Image, ImageAdmin)

class GaleryAdmin(admin.ModelAdmin):
    # SlugField
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Gallery, GaleryAdmin)


