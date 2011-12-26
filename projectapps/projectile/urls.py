# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from django.conf.urls.defaults import *
from django.contrib import admin
from django.views import generic


urlpatterns = patterns('projectile.views',
    url(r'^$', 'index', name='projectile--index-шшшш'),
    (r'^test/$', 'test_view'),

    (r'^projects/$', 'prj_list'),
    (r'^project-view/(?P<r_project>.*)/$', 'prj_view'),
    (r'^project-edit/(?P<r_project>.*)/$', 'prj_edit'),

    (r'^milestones/$', 'mlst_list'),
    (r'^milestone-view/(?P<r_project>.*)/(?P<r_milestone>.*)/$', 'mlst_view'),
    (r'^milestone-edit/(?P<r_project>.*)/$', 'mlst_edit'),

)
