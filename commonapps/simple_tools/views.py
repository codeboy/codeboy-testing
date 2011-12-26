# -*- coding: utf-8 -*-


from django.template import Context, loader, RequestContext
from django.http import Http404, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# для логгирования в debug_toolbar | info debug warning error critical
import logging

from procesors import custom_proc


#def custom_proc(request):
#
#    return {
#        'app': 'Common app',
#        'user': request.user,
#        'ip_address': request.META['REMOTE_ADDR']
#    }



#    SYSTEM
#==================================================
def index(request):
    from admin_tools.dashboard.modules import AppList

    t = loader.get_template('index.html')
    t_data = dict()

#    zz = AppList(title='Administration', models=('django.contrib.*'),)
#    print dir(zz)
#    print zz.include_list

    from django.contrib.admin.models import LogEntry
    qs = LogEntry.objects.all()
    print qs

#    t_data['brands'] = Brand.objects.filter(show_on_index=True)
    c = RequestContext(request, t_data, processors=[custom_proc])
    return HttpResponse(t.render(c))

def trash_view(request):
    t = loader.get_template('trash.html')
    c = RequestContext(request,{
    }, processors=[custom_proc])
    return HttpResponse(t.render(c))

def spare_parts(request):
    t = loader.get_template('spare_parts.html')
    c = RequestContext(request,{
    }, processors=[custom_proc])
    return HttpResponse(t.render(c))


# TODO: переделать под контекст
def report_view(request, code="chunks_error"):

    t = loader.get_template('report.html')
    c = RequestContext(request, {
        'code':code,
        }, processors=[custom_proc])
    return HttpResponse(t.render(c))



