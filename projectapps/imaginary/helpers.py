from django.contrib.admin import ModelAdmin
from admin_forms import ItemChangeForm


class GalAdmin(ModelAdmin):
    form = ItemChangeForm
    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site 
        super(GalAdmin, self).__init__(model, admin_site)
