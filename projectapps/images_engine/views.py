# -*- coding: utf-8 -*-


from django.template import Context, loader, RequestContext
from django.http import Http404, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# для логгирования в debug_toolbar | info debug warning error critical
import logging



def custom_proc(request):
    ''' Это контекстный процессор, он принимает объект HttpRequest,
    и возвращает словарь переменных для его последующего использования в контексте шаблона" '''
    return {
        'app': 'Common app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }



#    SYSTEM
#==================================================
def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request,{
    }, processors=[custom_proc])
    return HttpResponse(t.render(c))

