# -*- coding: utf-8 -*-
#

import os, sys

sys.stdout = sys.stderr
sys.path.insert(0, os.path.dirname(__file__))

sys.path.append('/home/stakos/www')
#sys.path.append( os.abspath('~/') )

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()


#
#import os, sys
#sys.path.insert(0, os.path.join(os.path.expanduser('~'), 'django'))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'имя_проекта.settings'
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()