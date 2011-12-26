from django import forms
from models import Mailer, MailerUsers, Filter

class MailerForm(forms.ModelForm):
    class Meta:
        model = Mailer
        exclude = ('start', 'end', 'count', 'filters', 'users', 'status',
                   'counter')


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
