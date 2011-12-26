# -*- coding: utf-8 -*-
from django import forms
from django.db.models import OneToOneRel, ManyToOneRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe

from models import Gallery, Image, GalleryRel


class GalleryThumbsWidget(forms.Select):
    def render(self, name, value, attrs=None):
        html = super(GalleryThumbsWidget, self).render(name, value, attrs)
        if value:
            gallery = Gallery.objects.get(id=value)
            images = Image.objects.filter(gallery=gallery)
            html += '<div id="id_gallery_images">'
            for image in images:
                html += image.admin_thumbnail_view()
            html += '</div>'
            html +='''
            <script type="text/javascript">
            $(document).ready(
                function() {

                images = $('#id_gallery_images');
                gallery = $('#id_gallery');
                gallery.change(function(){
                    value = gallery.val();
                    galleryChange(value);
                });

                var galleryChange = function(val){
                    var callback = function(request){
                        images.empty();
                        for(var x=0; x < request.length; x++ ){
                            var active = request[x];
                            images.append(active.admin_thumbnail_view);
                        };
                    };
                    galleryPost(val, callback);
                };

                var galleryPost = function(val, func){
                    $.post("/aj-gallery/", {
                        value : val,
                    },
                    function(data){
                        if (data == 'error'){
                            alert('error');
                        } else {
                            func(jQuery.parseJSON(data.dump));
                        }
                    }
                );
                };


            });
            </script>
            '''

        return mark_safe(html)

class ItemChangeForm(forms.ModelForm):
    gallery = forms.ModelChoiceField(queryset=Gallery.objects.all(),
        required=False, label='Галерея изображений', widget=GalleryThumbsWidget())
    def __init__(self, *args, **kwargs):
        super(ItemChangeForm, self).__init__(*args, **kwargs)
        rel = OneToOneRel(Gallery, 'gallery_id')
        self.fields['gallery'].widget = RelatedFieldWidgetWrapper(
            self.fields['gallery'].widget, rel, self.admin_site)
        if self.instance.pk:
            try:
                item_type = ContentType.objects.get_for_model(self.instance)
                gallery = GalleryRel.objects.filter(
                    content_type__pk=item_type.id, object_id=self.instance.id)
                if gallery:
                    self.fields['gallery'].initial = gallery[0].gallery.pk
            except GalleryRel.DoesNotExist, Gallery.DoesNotExist:
                pass
        else:
            self.fields['gallery'].widget = forms.Select(attrs={'disabled': 'disabled'})

    def save(self, *args, **kwargs):
        gall = self.cleaned_data['gallery']
        item = super(ItemChangeForm, self).save(*args, **kwargs)
        if gall:
            try:
                item_type = ContentType.objects.get_for_model(item)
                gallery = GalleryRel.objects.get(
                    content_type__pk=item_type.id, object_id=item.id)
                gallery.gallery = gall
                gallery.save()
            except GalleryRel.DoesNotExist:
                gallery = GalleryRel(content_object=item, gallery=gall)
                gallery.save()
                
        return item


class GalleryChangeForm(forms.ModelForm):
    images = forms.ModelMultipleChoiceField(required=False,
        queryset=Image.objects.none())
    def __init__(self, *args, **kwargs):
        super(GalleryChangeForm, self).__init__(*args, **kwargs)
        rel = ManyToOneRel(Image, 'images_id')
        self.fields['images'].widget = RelatedFieldWidgetWrapper(
            self.fields['images'].widget, rel, self.admin_site)
        if self.instance:
            self.fields['images'].queryset = Image.objects.filter(
                gallery=self.instance)
