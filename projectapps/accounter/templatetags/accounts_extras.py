# -*- coding: utf-8 -*-s

from django import template

register = template.Library()


@register.inclusion_tag('accounts_snippet_auth_status.html', takes_context=True)
def auth_status(context):
#    user = context['request']

    return {
#        'user' : user,
    }


@register.inclusion_tag('accounts_snippet_form_field.html', takes_context=True)
def render_form_field(context, form=0, style=None):

    return {
        'form': form,
#        'field' : field,
        'style' : style,
    }
