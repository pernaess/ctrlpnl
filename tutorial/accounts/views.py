# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .customScripts import Server_ping, SuccessfullInstall
from .models import ServerConnection, DatabaseConnection, NginxInstallation, PhpInstallation
from django.shortcuts import render, redirect
from .forms import (
     RegistrationForm,
     EditProfileForm,
     CreateRemoteDatabase,
     ConnectToServer,
     InstalledDatabaseForm,
     InstallNginx,
     InstallPhp,
     InstalledNginxForm
)
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
        print request.POST
        if 'create_server' in request.POST:
            createserverform = ConnectToServer(request.POST, prefix='createServer')
            if createserverform.is_valid():
                instance = createserverform.save(commit=False)
                instance.user = request.user
                instance.save()

                return redirect('accounts:ServicesView')
    else:
            nginxform = InstallNginx(prefix='nginx')
            phpform = InstallPhp(prefix='php')
            createdbform = CreateRemoteDatabase(prefix='createDB')
            createserverform = ConnectToServer(prefix='createServer')
            args = {
                'form1': createdbform,
                'form2': createserverform,
                'form3': nginxform,
                'form4': phpform}

            return render(request, 'accounts/services.html', args)


def createDBView(request):
    if request.method == 'POST':
        createdbform = CreateRemoteDatabase(request.POST, prefix='createDB')
        print createdbform.errors
        if createdbform.is_valid():
            playbook_path = ""
            database = createdbform.cleaned_data['database']
            if database == 'MySql':
                playbook_path = 'accounts/ansibleScripts/mysql.yml'
            elif database == 'PostgreSql':
                playbook_path = 'accounts/ansibleScripts/postgreSql.yml'
            user = request.user
            server = request.POST.getlist('createDB-server_name')
            if server[0] == 'all':
                server.pop(0)
            s_p = createdbform.cleaned_data['sudo_password']
            db_user = createdbform.cleaned_data['username']
            db_pass = createdbform.cleaned_data['password']
            db_name = createdbform.cleaned_data['database_name']
            p_o = run_playbook()
            p_o.run_pb(user, s_p, server, db_user, db_pass, db_name, playbook_path)
            c_i = SuccessfullInstall()
            createdbform.cleaned_data['username'] = 'Not stored'
            createdbform.cleaned_data['password'] = 'Not stored'
            createdbform.cleaned_data['database_name'] = 'Not stored'
            createdbform.cleaned_data['sudo_password'] = 'Not stored'
            instance = createdbform.save(commit=False)
            for items in server:
                check = c_i.check_install_db(p_o.pb_output(), items)
                if check:
                    exists = DatabaseConnection.objects.filter(server_name=items, database_name=db_name).exists()
                    if not exists:
                        instance.user = request.user
                        instance.server_name = items
                        instance.save()
                        print "Form saved"
                    else:
                        print 'Createdbform not saved'
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            return HttpResponse("Error: Something went wrong")


def aboutView(request):
    return render(request, 'accounts/about.html')


def dashboardView(request):
    squery = ServerConnection.objects.order_by('server_nickname').values_list('server_nickname', flat=True).distinct()
    ipquery = ServerConnection.objects.order_by('server_nickname').values_list('server_ip', flat=True).distinct()
    qresultList = []
    for index, item in enumerate(squery):
      qresult = {}
      qresult['servername'] = item
      qresult['ip'] = ipquery[index]
      qresultList.append(qresult)

    installed_db_form = InstalledDatabaseForm(prefix='installed_db')
    installed_nginx_form = InstalledNginxForm(prefix='installed_nginx')
    args= {'qresultList': qresultList, 'form1': installed_db_form, 'form2': installed_nginx_form}
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


def start_mysql_db(request):
    if request.method == 'POST':
        playbook_path = "accounts/ansibleScripts/modifyScripts/mysql/startMysql.yml"
        form = InstalledDatabaseForm(data=request.POST, prefix="installedDb")
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_db-servers')
            user = request.user
            empty = ""
            p_o = run_playbook()
            p_o.run_pb(user, empty, server, empty, empty, empty, playbook_path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def stop_mysql_db(request):
    if request.method == 'POST':
        playbook_path = "accounts/ansibleScripts/modifyScripts/mysql/stopMysql.yml"
        form = InstalledDatabaseForm(data=request.POST, prefix="installedDb")
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_db-servers')
            user = request.user
            empty = ""
            p_o = run_playbook()
            p_o.run_pb(user, empty, server, empty, empty, empty, playbook_path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def install_nginx(request):
    if request.method == 'POST':
        playbook_path = "accounts/ansibleScripts/nginx.yml"
        form = InstallNginx(data=request.POST, prefix="installedNginx")
        print "første"
        print form.errors
        if form.is_valid():
            print "andre"
            server = request.POST.getlist('nginx-servers')
            if server[0] == 'all':
                server.pop(0)
            user = request.user
            empty = ""
            p_o = run_playbook()
            p_o.run_pb(user, empty, server, empty, empty, empty, playbook_path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_nginx(p_o.pb_output(), items)
                instance = form.save(commit=False)
                if check:
                    exists = NginxInstallation.objects.filter(servers=items).exists()
                    if not exists:
                        instance.user = request.user
                        instance.servers = items
                        instance.save()
                        print "Form saved"
                    else:
                        print 'Createdbform not saved'
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def install_php(request):
    print "her"
    if request.method == 'POST':
        playbook_path = "accounts/ansibleScripts/php.yml"
        form = InstallPhp(data=request.POST, prefix="installedPhp")
        print "første"
        print form.errors
        if form.is_valid():
            print "andre"
            server = request.POST.getlist('php-servers')
            if server[0] == 'all':
                server.pop(0)
            user = request.user
            empty = ""
            p_o = run_playbook()
            p_o.run_pb(user, empty, server, empty, empty, empty, playbook_path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_php(p_o.pb_output(), items)
                instance = form.save(commit=False)
                if check:
                    exists = PhpInstallation.objects.filter(servers=items).exists()
                    if not exists:
                        instance.user = request.user
                        instance.servers = items
                        instance.save()
                        print "Form saved"
                    else:
                        print 'Createdbform not saved'
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")