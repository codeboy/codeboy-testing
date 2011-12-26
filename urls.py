# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views import generic
from django.http import Http404
import os


admin.autodiscover()


#raise Http404

PROJECT_DIR= os.path.abspath(os.path.dirname(__file__))
#request.META.get




urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^admin_tools/', include('admin_tools.urls')),
#    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': localmedia}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(PROJECT_DIR, 'media')}),

    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^comments/', include('django.contrib.comments.urls')),
)



### some cool shit
urlpatterns += patterns('simple_tools.views',
    (r'^$', 'index'),
    (r'^trash/$', 'trash_view'),
#    (r'^spare_parts/$', 'spare_parts'),
)


#####   Messages   #####
urlpatterns += patterns('',
    (r'^report/$', 'commonapps.simple_tools.views.report_view'),
    (r'^report/(?P<code>.*)/$', 'commonapps.simple_tools.views.report_view'),
    (r'^messages/', include('commonapps.messages.urls')),
#    (r'^messages/inbox/', 'commonapps.messages.views.inbox'),
    (r'^projectile/', include('projectapps.projectile.urls')),
)



#####   Accounts   #####
#urlpatterns += patterns('accounts_engine.views',
#    (r'^login/$', 'login_view'),
#    (r'^logout/$', 'logout_view'),
#)

#####   AJAX   #####
#urlpatterns += patterns('',
#    (r'^aj-carform/$', 'catalog_engine.js_response.car_work'),
#)
