# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader, RequestContext
from django.core.urlresolvers import reverse
from projectapps.accounter.models import CustomUser
from projectapps.catalog_engine.models import Brand
from projectapps.tags_e.models import Tag
from procesors import custom_proc

from models import Mailer, Filter, MailerUsers
from forms import MailerForm, FilterForm

from utils import send_mail2


def mailer_all_view(request):
    if not request.user.is_superuser:
        raise Http404

    template = 'mailer_all.html'
    data = dict()
    data['mailers'] = Mailer.objects.all().order_by('-id')
    t = loader.get_template(template)
    c = RequestContext(request, data, processors=[custom_proc])
    return HttpResponse(t.render(c))


def mailer_add_view(request):
    if request.user.is_superuser:
        template = "mailer_add.html"
        data=dict()
        if request.method == 'POST':
            mailer_form = MailerForm(request.POST)
            filter_form = FilterForm(request.POST)
            if mailer_form.is_valid() and filter_form.is_valid():
                filt = filter_form.save()
                mailer = mailer_form.save(commit=False)
                mailer.filters = filt
                mailer.save()
                return HttpResponseRedirect(reverse('mailer_all'))
            else:
                data['mailer_form'] = MailerForm(request.POST)
                data['filter_form'] = FilterForm(request.POST)
                t = loader.get_template(template)
                c = RequestContext(request, data, processors=[custom_proc])
                return HttpResponse(t.render(c))
        else:
            data['mailer_form'] = MailerForm()
            data['filter_form'] = FilterForm()
            t = loader.get_template(template)
            c = RequestContext(request, data, processors=[custom_proc])
            return HttpResponse(t.render(c))
    else:
        raise Http404


def mailer_start_view(request, mailer_id):
    if not request.user.is_superuser:
        raise Http404
    try:
        mailer = Mailer.objects.get(id=int(mailer_id))
    except Mailer.DoesNotExist, KeyError:
        raise Http404
    mailer.status = 'STR'
    mailer.save()
#    mailer.send_mail()
    return HttpResponseRedirect(reverse('mailer_all'))

def mailer_start(request):
    if not request.user.is_superuser:
        raise Http404
    started_mailers = Mailer.objects.filter(status='STR')
    for mailer in started_mailers:
        mailer.send()
    return HttpResponseRedirect(reverse('mailer_all'))

def mailer_view(request, mailer_id):
    if not request.user.is_superuser:
        raise Http404
    data = dict()
    template = "mailer.html"
    try:
        mailer = Mailer.objects.get(id=int(mailer_id))
    except Mailer.DoesNotExist, KeyError:
        raise Http404
    data['mailer'] = mailer
    data['users'] = MailerUsers.objects.select_related().filter(mailer=mailer)
    t = loader.get_template(template)
    c = RequestContext(request, data, processors=[custom_proc])
    return HttpResponse(t.render(c))
