# -*- coding: utf-8 -*-


from django.template import Context, loader, RequestContext
from django.http import Http404, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from django.core import serializers

from models import Gallery, Image

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


def js_response(request):
    message = ''
    # если запрос аякс
    if request.is_ajax():

        if request.method == 'GET':
            message = 'Only POST allowed here!'

        # и если метод пост
        elif request.method == 'POST' and request.POST.has_key('value'):
            try:
                value = int(request.POST.get('value'))
                gallery = Gallery.objects.get(id=value);
                images = Image.objects.filter(gallery=gallery)

                dump = list()
                for image in images:
                    dic = dict()
                    dic['pk'] = str(image.pk)
                    dic['admin_thumbnail_view'] = image.admin_thumbnail_view()
                    dump.append(dic)
    
                dump = simplejson.dumps(dump)
                callback = request.GET.get('callback', '')
                req = dict()
                req['dump'] = str(dump)
                response = simplejson.dumps(req)

                return HttpResponse(response, mimetype="application/json")
            except Gallery.DoesNotExist, ValueError:
                return HttpResponse('error')

