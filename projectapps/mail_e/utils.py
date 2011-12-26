# -*- coding: utf-8 -*-

from django.core.mail import send_mail as send
from django.core.mail import EmailMultiAlternatives
from base64 import b64encode

from smtplib import SMTPRecipientsRefused
from django.template.loader import get_template
from django.template import Context

def send_mail(email_to, subject, content):
    try:
        snd = send(subject, content, 'noreply@arobase.ru', email_to)
    except SMTPRecipientsRefused:
        snd = 0
    return snd

def send_mail2(email_to, subject, content):
    try:
#        snd = send(subject, content, 'noreply@arobase.ru', email_to)

        subject, from_email, to = subject, 'robot@arobase.ru', email_to
        text_content = content
        html_content = '<p>'+content.replace('\n', '<br/>\n')+'</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        snd = msg.send()

    except SMTPRecipientsRefused:
        snd = 0
    return snd


def send_mail3(email_to, subject='tmp', content=None, choice='NEW'):
    try:
#        snd = send(subject, content, 'noreply@arobase.ru', email_to)

#        TEMPLATE_CHOICES = {
#                            'NEW': 'new_message',
#                            'REG': 'registration',
#                            'ORD': 'order',
#                            }

#        plaintext = get_template(TEMPLATE_CHOICES[choice] + '.txt')
#        html     = get_template(TEMPLATE_CHOICES[choice] + '.html')

#        data = Context({ 'username': 'vapask' })

#        text_content = plaintext.render(data)
#        html_content = html.render(data)

        subject, from_email, to = subject, 'robot@arobase.ru', email_to
        import markdown
        md = markdown.Markdown(safe_mode='remove')
        print md.convert(content)
        text_content = content
        html_content = content.replace('\n', '<br/>\n')
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        snd = msg.send()

    except SMTPRecipientsRefused:
        snd = 0
    return snd
