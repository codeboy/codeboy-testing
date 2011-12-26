# -*- coding: utf-8 -*-

from django.template import Context, loader, RequestContext
from django.http import Http404, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template.defaultfilters import slugify
from django.contrib import messages


from django.utils.translation import ugettext_lazy as _

import logging
from pytils import translit
from random import randint
import hashlib

from projectapps.images_engine.models import Image
from procesors import custom_proc
from projectapps.mail_e.utils import send_mail

from models import Project, Component, Milestone, Task, TaskStates
from forms import ProjectEditForm, MilestoneEditForm






def index(request):
    """
    вывод всех проектов
    """
    template = 'prjctl_base.html'
    data = dict()

    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



#####   PROJECTS   ######################################################
def prj_list(request):
    """
    вывод всех проектов
    """
    template = 'prjctl_prj_list.html'
    data = dict()

    try:
        q_projects = Project.objects.all().order_by('datetime_modifed')

        data['list'] = q_projects
    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Нету! ((', fail_silently=True)


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



def prj_view(request, r_project):
    """
    просмотр информаци о проекте
    """
    template = 'prjctl_prj_view.html'
    data = dict()

    try :
        q_project = Project.objects.get(name_slug = r_project)
        data['var'] = q_project

    except Project.DoesNotExist :
        messages.add_message(request, messages.ERROR, 'Project does not exist ((', fail_silently=True)

    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



@login_required()
@csrf_protect
def prj_edit(request, r_project):
    """
    редактирование проекта
    """
    template = 'prjctl_prj_edit.html'
    data = dict()

    try:
        q_project = Project.objects.get(name_slug=r_project)
        data['var'] = q_project
        if request.method == 'POST':
            form = ProjectEditForm(request.POST, instance=q_project)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect ('/projectile/project-view/%s' % q_project.name_slug)
            else:
                data['form'] = ProjectEditForm(request.POST, instance=q_project)
        else:
            data['form'] = ProjectEditForm(instance=q_project)


    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Нету! ((', fail_silently=True)

    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))





#####   MILESTONES   ####################################################
def mlst_list(request):
    """
    вывод всех вех (milestones)
    """
    template = 'prjctl_mlst_list.html'
    data = dict()

    try:
        q_list = Milestone.objects.all().order_by('project__name_slug', 'datetime_modifed')

        data['list'] = q_list
    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Нету! ((', fail_silently=True)


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



def mlst_view(request, r_project, r_milestone):
    """
    просмотр информаци о вехе
    """
    template = 'prjctl_mlst_view.html'
    data = dict()

    try :
        q_project = Project.objects.get(name_slug = r_project)
        data['project'] = q_project

        try:
            q_milestone = Milestone.objects.get(name_slug = r_milestone, project = q_project)
            data['var'] = q_milestone

        except Milestone.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Milestone does not exist!', fail_silently=True)

    except Project.DoesNotExist :
        messages.add_message(request, messages.ERROR, 'Project does not exist!', fail_silently=True)


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



@login_required()
@csrf_protect
def mlst_edit(request, r_project, r_milestone):
    """
    редактирование вехи
    """
    template = 'prjctl_prj_edit.html'
    data = dict()

    try:
        q_project = Project.objects.get(name_slug=r_project)
        data['var'] = q_project
        if request.method == 'POST':
            form = ProjectEditForm(request.POST, instance=q_project)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect ('/projectile/project-view/%s' % q_project.name_slug)
            else:
                data['form'] = ProjectEditForm(request.POST, instance=q_project)
        else:
            data['form'] = ProjectEditForm(instance=q_project)


    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Нету! ((', fail_silently=True)

    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))




#####   COMPONENT   #################################################
def cmpt_list(request):
    """
    """
    template = 'prjctl_prj_list.html'
    data = dict()

    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))


#@login_required()
def cmpt_view(request):
    """
    """
    template = 'prjctl_prj_list.html'
    data = dict()


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



@login_required()
def cmpt_edit(request):
    """
    """
    template = 'prjctl_prj_list.html'
    data = dict()


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



#####   TASK   ###################################################
def task_list(request):
    """
    """
    template = 'prjctl_prj_list.html'
    data = dict()

    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))


#@login_required()
def task_view(request):
    """
    """
    template = 'prjctl_prj_list.html'
    data = dict()


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



@login_required()
def task_edit(request):
    """
    """
    template = 'prjctl_prj_list.html'
    data = dict()


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))






def test_view(request):

    t = loader.get_template('prjctl_base.html')
    c = RequestContext(request,{
        'logz' : logz,
    }, processors=[custom_proc])
    return HttpResponse(t.render(c))


