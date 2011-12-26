# -*- coding: utf-8 -*-
#========================================================
#
#   Project
#       name : codeboy.ru
#       customer : codeboy.ru
#       developer : codeboy.ru
#       version : 0.0.1
#
#   Технические особенности :
#       Python 2.6
#       Python modules:
#           django-admin-tools = http://bitbucket.org/izi/django-admin-tools/wiki/Home
#           PIL: http://www.pythonware.com/products/pil/
#           Markdown = http://pypi.python.org/packages/source/M/Markdown/Markdown-2.0.3.tar.gz
#           django-imagekit = http://bitbucket.org/jdriscoll/django-imagekit/wiki/Home
#           pytils = https://github.com/j2a/pytils  ||  http://pypi.python.org/pypi/pytils
#           BeautifulSoup = http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.0.8.1.tar.gz
#
#           django-easytree = http://bitbucket.org/fivethreeo/django-easytree/wiki/Home
#               идёт с проектом, но можно и установить
#
#           django-css = https://github.com/dziegler/django-css
#
#
#========================================================
### GLOBAL TODO: 3\0
#       TODO: images_engine - переделать: удаление совместных картинок
#       TODO: storage backend - свои стораджи данных
#       TODO: УДАЛЕНИЕ СВЯЗАННЫХ ОТНОШЕНИЙ!!!! КАРТИНКИ И АДРЕСА!!!!!
#       TODO: Чистка корзин
#       TODO: Чистка сессий
#       TODO: Оптимизировать запросы для корзины!!!!!
#
#========================================================

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

import os, sys, platform

# for hot change paths
# TODO: ref or delete this part
if "Windows" in platform.system():
    import set_local as customSettings
else :
    import set_local as customSettings


PROJECT_DIR= os.path.abspath(os.path.dirname(__file__)) # Path to prj
sys.path.append(os.path.join(PROJECT_DIR, 'projectapps')); # add to apps search path
sys.path.append(os.path.join(PROJECT_DIR, 'commonapps')); # add to apps search path


#####   DATABASE SETINGS   #####
DATABASES = {
    'default': {
        'NAME':         customSettings.DATABASE_NAME,
        'ENGINE':       customSettings.DATABASE_ENGINE,
        'USER':         customSettings.DATABASE_USER,
        'PASSWORD':     customSettings.DATABASE_PASSWORD,
        'HOST' :        customSettings.DATABASE_HOST,
        'PORT' :        customSettings.DATABASE_PORT,
    }
}



#####   PROJECT SETTINGS   #####
DEFAULT_CHARSET = 'utf8'
TIME_ZONE = 'Europe/Moscow'
LANGUAGES = (
      ('ru', ('russian')),
#      ('en', _('English')),
)

LANGUAGE_CODE = 'ru-ru'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = 'p1*jci5tw)g77-wpv6x&vsif!jkyz#ov425&g67w8zd!dubjff'

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
CACHE_BACKEND = 'locmem://'
#CACHE_BACKEND = 'dummy:///'
#CACHE_MIDDLEWARE_SECONDS = 0

DEBUG = customSettings.DEBUG
#DEBUG = True
#DEBUG = False
ADMINS = ()
ADMIN_LOGIN = 'admin'
ADMIN_PASSWORD = 'sha1$78721$990bc1fa2047d435dbe680f09730239c2af4938c'
MANAGERS = ADMINS


#AUTH_PROFILE_MODULE = 'accounts_engine.UserProfile'
AUTHENTICATION_BACKENDS = (
#    'auth_backends.CustomUserModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)
#CUSTOM_USER_MODEL = 'accounts_engine.CustomUser'
LOGIN_URL = '/login/'


#####   URLs   #####
ROOT_URLCONF = 'urls'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin_media/'


#####   TEMPLATE SETINGS   #####
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
TEMPLATE_DIRS = (
        os.path.join(PROJECT_DIR, 'templates'),
)


#####   MIDDLEWARE   #####
MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


#####   CONTEXT PROCESSORS   #####
TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',

    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


#####   APPLICATIONS   #####
INSTALLED_APPS = (
    'debug_toolbar',

    # for django-admin-tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.comments',
#    'django.contrib.markup',
    'django.contrib.admindocs',

#    'tagging',
#    'compressor',

    'simple_tools',
    'messages',
    'ckeditor',

    'accounter',
    'imaginary',
    'projectile'
)




# TODO: why i need this???
#####   TEST SETTINGS   #####
MAPS_API_KEY = 'ABQIAAAABdHuQzfLcNwgKwRN3Q2l8BS9eAW-oERH4EKaCahp9H4R-3FLPhThQsSqkFdzJxtTp_F5EnY3IowrNA'


# for django-admin-tools
#ADMIN_TOOLS_MEDIA_URL = os.path.join(PROJECT_DIR, 'admin_tools/media')

FIXTURE_DIRS = (os.path.join(PROJECT_DIR, 'fixtures'),)
INTERNAL_IPS = ('127.0.0.1',)

CKEDITOR_MEDIA_PREFIX = "/media/ckeditor/"
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')

def custom_show_toolbar(request):
#    val = False
#    import socket
#    ips =  socket.gethostbyname_ex(socket.gethostname())[2]
#    print ips
#    if '192.168' in ips:
#        val = True
#
#    return val


    return False
#    return True
#    return customSettings.DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS':      False,
    'SHOW_TOOLBAR_CALLBACK':    False,
    'SHOW_TEMPLATE_CONTEXT':    True,
    'SHOW_TOOLBAR_CALLBACK':    custom_show_toolbar,
#    'EXTRA_SIGNALS':            ['myproject.signals.MySignal'],
    'HIDE_DJANGO_SQL':          False,
#    'TAG':                      'div',
    }
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)



# secret
# https://websvn.bein.loc/svn/stakos/
# 77.239.243.34 | 84.52.118.15
# maxim | Q4m*XjL#


# dumpdata pages_engine --indent 4 >> fixt_pages_engine.json
# loaddata fixt_pages_engine.json

