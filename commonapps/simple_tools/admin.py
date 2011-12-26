# -*- coding: utf-8 -*-
# admin.py for

# SYSTEMS
from django.contrib import admin

# MODELS
'''from commonapp.models import Post, Category, Tag, Pages


class PostAdmin(admin.ModelAdmin):
    # SlugField
    prepopulated_fields = {"name_slug": ("name",)}

    save_on_top = True
admin.site.register(Post, PostAdmin)
# - - - - - - - - - - - - - - - - - - - - - - - - -


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}

    save_on_top = True
admin.site.register(Category, CategoryAdmin)
# - - - - - - - - - - - - - - - - - - - - - - - - -


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}

    save_on_top = True
admin.site.register(Tag, TagAdmin)
# - - - - - - - - - - - - - - - - - - - - - - - - -


class PagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}

    save_on_top = True
admin.site.register(Pages, PagesAdmin)
# - - - - - - - - - - - - - - - - - - - - - - - - -
'''