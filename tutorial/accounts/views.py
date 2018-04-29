# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .customScripts import Server_ping
from .models import ServerConnection
from django.shortcuts import render, redirect
from .forms import (
     RegistrationForm,
     EditProfileForm,
     CreateRemoteDatabase,
     ConnectToServer,
     ajaxForm,
     ConnCheck
)
import json
from django.http import HttpResponse
from django.http import JsonResponse
from .ansibleScripts.run_playbooks import run_playbook
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')
    else:
        form = RegistrationForm()
        args = {'form': form}

        return render(request, 'accounts/reg_form.html', args)


def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('accounts:view_profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:view_profile')

        else:
            return redirect('accounts:change_password')

    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


# Handles forms in services.html based on form submitted
def ServicesView(request):
    if request.method == 'POST':
        if 'create_db' in request.POST:
            createdbform = CreateRemoteDatabase(request.POST, prefix='createDB')
            print createdbform.errors
            if createdbform.is_valid():
                user = request.user
                server = createdbform.cleaned_data['server_name']
                s_p = createdbform.cleaned_data['sudo_password']
                db_user = createdbform.cleaned_data['username']
                db_pass = createdbform.cleaned_data['password']
                db_name = createdbform.cleaned_data['database_name']
                p_o = run_playbook()
                p_o.run_pb(user, s_p, server, db_user, db_pass, db_name)
                createdbform = CreateRemoteDatabase(prefix='createDB')
                createserverform = ConnectToServer(prefix='createServer')
                context = {
                    'form1': createdbform,
                    'form2': createserverform,
                    'p_output': p_o.pb_output(),
                    't_output': p_o.r_time()
                }
                return render(request, 'accounts/services.html', context)


        elif 'create_server' in request.POST:
            createserverform = ConnectToServer(request.POST, prefix='createServer')
            if createserverform.is_valid():
                instance = createserverform.save(commit=False)
                instance.user = request.user
                instance.save()

                return redirect('accounts:ServicesView')
    else:
            createdbform = CreateRemoteDatabase(prefix='createDB')
            createserverform = ConnectToServer(prefix='createServer')
            args = {'form1': createdbform, 'form2': createserverform}

            return render(request, 'accounts/services.html', args)


def aboutView(request):
    return render(request, 'accounts/about.html')


def dashboardView(request):
    squery = ServerConnection.objects.order_by('server_nickname').values_list('server_nickname', flat=True).distinct()
    ipquery = ServerConnection.objects.order_by('server_nickname').values_list('server_ip', flat=True).distinct()
    #ping = Server_ping()
    #status = ping.server_status(ipquery)
    conc = ConnCheck(request.POST, prefix='connCheck')
    qresultList = []
    for index, item in enumerate(squery):
      qresult = {}
      qresult['servername'] = item
      qresult['ip'] = ipquery[index]
      #qresult['status'] = status[index]
      qresultList.append(qresult)

    args= {'qresultList': qresultList, 'ajaxForm': ajaxForm, 'conForm': conc}
    return render(request, 'accounts/dashboard.html', args)


def CheckConn(request):
    if request.method == 'POST':
        ipquery = ServerConnection.objects.order_by('server_nickname').values_list('server_ip', flat=True).distinct()
        ping = Server_ping()
        status = ping.server_status(ipquery)
        print('Inside')
        return JsonResponse(status, safe=False)
    else:
        print('fæææn')
        return HttpResponse("Ain't working")


def testAjax(request):
    if request.method == 'POST':
        formAjax = ajaxForm(request.POST, prefix='ajaxTest')
        print formAjax.errors
        if formAjax.is_valid():
            label = 'Dette blir sendt fra server! AJAAAAAAAAAX!!!!'
            print(label)
            print('to')
            data = {
                'change': label
            }
            print(data)
            return JsonResponse(data)
        else:
          print('fæææn')
          return HttpResponse("Form is not valid")
