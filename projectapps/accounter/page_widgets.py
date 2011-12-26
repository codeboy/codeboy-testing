# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.conf import settings


# виджет для поля визуального выбора карты
class LocationPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.MEDIA_URL + 'css/location_picker.css',
            )
        }
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            'http://www.google.com/jsapi?key=' + settings.MAPS_API_KEY,
            settings.MEDIA_URL + 'js/jquery.location_picker.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)

class LocationField(models.CharField):

    def formfield(self, **kwargs):
        kwargs['widget'] = LocationPickerWidget
        return super(LocationField, self).formfield(**kwargs)


#class ShopTools():
#    """Tools class"""
def get_lat_long(location):
      """a function that converts the location address to it's longitude and latitude"""
      import urllib

      key=settings.MAPS_API_KEY
      output = 'csv'
      location=urllib.quote_plus(location.encode('utf-8'))
      request = "http://maps.google.com/maps/geo?q=%s&output=%s&sensor=false&key=%s" % (location, output, key)
      data=urllib.urlopen(request).read()
      dlist=data.split(',')
      if dlist[0]=='200':
        return dlist[2],dlist[3]
      else:
        return 0,0
