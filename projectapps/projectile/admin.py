# -*- coding: utf-8 -*-
# admin.py for catalog_engine

from django.contrib import admin

from commonapps.treebeard.admin import TreeAdmin

from models import Project, Milestone, Component, Task, TaskStates


class SimpleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(Project, SimpleAdmin)
admin.site.register(Milestone, SimpleAdmin)
admin.site.register(Component, SimpleAdmin)

class TreeExampleAdmin(TreeAdmin):
    def save_form(self, request, form, change):
        return form.save(commit=False)
class MP_Admin(TreeExampleAdmin):
    pass
admin.site.register(Task, MP_Admin)

class TaskStatesAdmin(admin.ModelAdmin):
#    prepopulated_fields = {"name_slug": ("name",)}
    save_on_top = True
admin.site.register(TaskStates, TaskStatesAdmin)
