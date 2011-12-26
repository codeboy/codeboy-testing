# -*- coding: utf-8 -*-


from django.template import Context, loader, RequestContext
from django.http import Http404, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.contrib.auth.tokens import default_token_generator


import logging
from pytils import translit
from random import randint
import hashlib
import datetime

from models import CustomUser, Address, PhoneStatus, IpBan
from forms import CustomUserForm, RegistrationForm, AdressForm, PasswordResetRequestForm, SetPasswordForm

from projectapps.imaginary.models import Image
#from commonapps.messages.models import Ticket
from procesors import custom_proc
from p_utils import send_mail, phone_formater, send_sms, phone_validate_util, page_message


#    SYSTEM
#==================================================
def index(request):
    return HttpResponseRedirect('/')


def login_view(request):
    template = 'ace_login_view.html'
    data = dict()

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        q_ipban = False

        try:
            q_ipban = IpBan.objects.get(ipaddress = request.META['REMOTE_ADDR'])
            if q_ipban.count >= 5 :
                timedelta = datetime.datetime.now() - q_ipban.datetime
                timedelta = str(timedelta).split(',')
                if not len(timedelta) > 1:
                    td1 = str(timedelta[0]).split(':')
                    if int(td1[0]) < 1:
                        if int(td1[1]) < 30:
                            page_message(request, 41, None, 'error')
    #                        return HttpResponseRedirect('/login/')
                            return HttpResponseRedirect('/report/login-falsee/')
                        else:
                            q_ipban.delete()
                            IpBan.objects.get(ipaddress = request.META['REMOTE_ADDR']).delete()
#                            return HttpResponseRedirect('/login/')
                            q_ipban = False
                    else:
                        q_ipban.delete()
#                        return HttpResponseRedirect('/login/')
                        q_ipban = False
                else:
                    q_ipban.delete()

        except IpBan.DoesNotExist:
            pass


        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            try:
                qq_ipban = IpBan.objects.get(ipaddress = request.META['REMOTE_ADDR'])
                qq_ipban.count = q_ipban.count + 1
#                qq_ipban.datetime = datetime.datetime.now()
                qq_ipban.save()
            except IpBan.DoesNotExist:
                s_ipban = IpBan(
                    ipaddress = request.META['REMOTE_ADDR'],
                    datetime = datetime.datetime.now(),
                    count = 1
                )
                s_ipban.save()
            page_message(request, 40, None, 'error')
            return HttpResponseRedirect('/login/')
    else:


        t = loader.get_template(template)
        c = RequestContext(request,data, processors=[custom_proc])
        return HttpResponse(t.render(c))




def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_protect
def password_reset(request):
    '''
    форма запроса восстановления пароля
    принмает POST email
    записывает в activation_code хеш
    отправляет письмо
    '''
    template = 'accounts_password_reset.html'
    data = dict()



#    form = PasswordResetRequestForm(request.POST)

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            login = request.POST['login']

            try:
                q_user = CustomUser.objects.get(username=login)

                h = hashlib.new('ripemd160')
                h.update("%s%s" % (q_user.username.encode("utf-8"), q_user.email.encode("utf-8")))
                code_hash = h.hexdigest()

                content = u'''
Здравствуйте!
Кто-то, возможно вы, запросили восстановление пароля.
Если это так, то перейдите по этой ссылке:
http://62.109.9.197/password-reset-confirm/%s
Вам будет предложено вести новый пароль.

Если же вы не запрашивали изменение пароля, то просто поригнорируйте это письмо.
''' % (code_hash)
                send_mail([q_user.email,],
                    'Восстановление пароля на сайте stakos.ru', content)

                q_user.activation_code = code_hash
                q_user.save()

                messages.add_message(request, messages.INFO,
                    'Вам отправлено письмо с кодом.', fail_silently=True)


            except CustomUser.DoesNotExist:
                messages.add_message(request, messages.INFO, 'Что-то не так!', fail_silently=True)
                form = PasswordResetRequestForm(request.POST)

        else:
            data['form'] = PasswordResetRequestForm(request.POST)
    else:
        form = PasswordResetRequestForm()
    data['form'] = form


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))



@csrf_protect
def password_reset_confirm(request, confirm_code):
    '''
    контрол восстановления пароля
    принмает строку с хешем,
    при валидности отдаёт форму для сброса пароля
    '''
    template = 'accounts_password_change.html'
    data = dict()


    try:
        q_user = CustomUser.objects.get(activation_code=confirm_code)

        if request.method == 'POST':
            form = SetPasswordForm(q_user, request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'пароль изменён', fail_silently=True)
                template = 'accounts_password_change_done.html'
            else:
                form = SetPasswordForm(q_user, request.POST)
        else:
            form = SetPasswordForm(q_user)

        data['form'] = form

    except CustomUser.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Что-то не так!', fail_silently=True)

    data['confirm_code'] = confirm_code


    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))




@login_required()
def phone_validate(request):
    template='accounts_phone-validate.html'
    data=dict()


    data['phone'] = phone_formater(request.user.phone_mobile)

    if request.method == 'POST':
        if request.POST.get('code_sms'):
            random_var = randint(1000, 9999)
            sms_result = send_sms('+7%s' % data['phone'], str(random_var))
            sms_id, sms_status = sms_result.split('=')

            if sms_status == 'accepted':
                try:
                    q_status = PhoneStatus.objects.get(user = request.user)
                    q_status.phone_num = data['phone']
                    q_status.phrase = random_var
                    q_status.sms_id = sms_id
                    q_status.sms_status = sms_status
                    q_status.save()
                except PhoneStatus.DoesNotExist:
                    q_status = PhoneStatus(
                        user = request.user,
                        phone_num = data['phone'],
                        phrase = random_var,
                        sms_id = sms_id,
                        sms_status = sms_status
                    )
                    q_status.save()

                    data['code_go'] = True
            else:
                page_message(request, 71, None, 'error')
                return HttpResponseRedirect('/profile/')

            data['code_go'] = True


        if request.POST.get('code_submit'):
            code = request.POST.get('code_input')

            q_status = PhoneStatus.objects.get(user = request.user)
            if q_status.phrase == code:
                q_user = CustomUser.objects.get(id = request.user.id)
                q_status = PhoneStatus.objects.get(user = request.user)
                q_user.phone_mobile_status = True
                q_user.save()
#                q_status.delete()

                page_message(request, 72, None, 'info')
                return HttpResponseRedirect('/profile/')

            else:
                page_message(request, 73, None, 'error')
                data['code_go'] = True


    else :
        if request.user.phone_mobile_status:
            return HttpResponseRedirect('/profile/')

        if len(data['phone']) <= 9:
            data['phone_error'] = True

        try:
            q_status = PhoneStatus.objects.get(user = request.user)
            if len(q_status.phrase) >=1:
                data['code_go'] = True
        except PhoneStatus.DoesNotExist:
            pass



    t = loader.get_template(template)
    c = RequestContext(request,data, processors=[custom_proc])
    return HttpResponse(t.render(c))




@login_required()
@phone_validate_util
def profile_view(request):
    '''
        отображает профиль пользователя
        id берётся из request
    '''

    try:
        user = CustomUser.objects.get(username = request.user.username)
    except CustomUser.DoesNotExist:
        user = ''
    if not user.is_staff:
        t = loader.get_template('accounts_profile_view.html')
        data = _orders_history_list(request)
        if not data.has_key('list'):
            data['list'] = list()
        if not data.has_key('statuses'):
            data['statuses'] = ''
        messages_list = Ticket.objects.filter(user__pk=request.user.pk).order_by('closed', '-important', '-last_updated').select_related()[:5]
        c = RequestContext(request,{
            'current_user' : user,
            'messages_list': messages_list,
            'list': data['list'][:5],
            'statuses': data['statuses'],
        }, processors=[custom_proc])
    else:
        return manager_view(request, user)
    return HttpResponse(t.render(c))



# TODO: image size min\max
@login_required()
def profile_edit(request):
    '''
        редактирование профиля
        id берётся из request
    '''
    if request.method == 'POST':
        user = CustomUser.objects.get(username = request.user.username)
        form_profile = CustomUserForm(request.POST, request.FILES, instance=user)
        if form_profile.is_valid():
            f = form_profile.save(commit=False)


            f.save()
            messages.add_message(request, messages.INFO, 'Информация сохранена.', fail_silently=True)
#            template = 'accounts_profile_view.html'\
            return HttpResponseRedirect('/profile/')

        else:
            form_profile = CustomUserForm(request.POST, request.FILES)
            messages.add_message(request, messages.INFO, 'Что-то не так!')
            template = 'accounts_profile_edit.html'

    else:
        try: user = CustomUser.objects.get(username = request.user.username)
        except : raise Http404
        template = 'accounts_profile_edit.html'

        form_profile = CustomUserForm(instance=user)


    t = loader.get_template(template)
    c = RequestContext(request,{
        'current_user' : user,
        'form_profile' : form_profile,
    }, processors=[custom_proc])
    return HttpResponse(t.render(c))




def registration_view(request):
    """
        регистрация
        форма регистрации короткая, только обязательные поля
        пароль сохраняется в два этапа: сохранение пользователя, зтем установка пароля
        при удаче переход на редактирование профиля
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            u = CustomUser.objects.get(pk = f.id)
            u.set_password(request.POST.get('password'))
            u.save()
        else:
            form = RegistrationForm(request.POST, request.FILES)

    else:
        form = RegistrationForm()

    t = loader.get_template('accounts_registration.html')
    c = RequestContext(request,{
#        'current_user' : user,
        'form' : form,
    }, processors=[custom_proc])
    return HttpResponse(t.render(c))


