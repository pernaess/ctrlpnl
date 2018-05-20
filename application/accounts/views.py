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
     InstalledNginxForm,
     InstalledPostgresForm,
     InstalledPhpForm
)
import time
from django.db import models
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
                # sudo_user = createserverform.cleaned_data['sudo_user']
                # ip = createserverform.cleaned_data['server_ip']
                # s_p = createserverform.cleaned_data['sudo_password']
                # path = "accounts/ansibleScripts/add-ssh-key.yml"
                # pb = run_playbook()
                # pb.run_pb_initial_connection(sudo_user, ip, s_p, path)
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
            print database
            for items in server:
                check = c_i.check_install_db(p_o.pb_output(), items)
                if check:
                    query = DatabaseConnection.objects.filter(server_name=items, database=database)
                    exists = query.exists()
                    if not exists:
                        instance.pk = None
                        instance.user = request.user
                        instance.server_name = items
                        print items
                        print instance
                        instance.save()
                        query.update()
                        time.sleep(2)
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
    installed_postgres_form= InstalledPostgresForm(prefix="installed_postgres")
    installed_php_form = InstalledPhpForm(prefix="installed_php")
    args= {
      'qresultList': qresultList,
      'form1': installed_db_form,
      'form2': installed_nginx_form,
      'form3': installed_postgres_form,
      'form4': installed_php_form
    }
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
        path = "accounts/ansibleScripts/modifyScripts/mysql/startMysql.yml"
        form = InstalledDatabaseForm(data=request.POST, prefix="installedDb")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_db-servers')
            s_p = request.POST.getlist('installed_db-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
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
        path = "accounts/ansibleScripts/modifyScripts/mysql/stopMysql.yml"
        form = InstalledDatabaseForm(data=request.POST, prefix="installedDb")
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_db-servers')
            s_p = request.POST.getlist('installed_db-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def restart_mysql_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/mysql/restartMysql.yml"
        form = InstalledDatabaseForm(data=request.POST, prefix="installedDb")
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_db-servers')
            s_p = request.POST.getlist('installed_db-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def uninstall_mysql_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/mysql/uninstallMysql"
        form = InstalledDatabaseForm(data=request.POST, prefix="installedDb")
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_db-servers')
            s_p = request.POST.getlist('installed_db-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_db(p_o.pb_output(), items)
                if check:
                    query = DatabaseConnection.objects.filter(server_name=items, database="MySql")
                    exists = query.exists()
                    print exists
                    if exists:
                        query.delete()
                        del query
                        print "Deleted"
                    else:
                        print 'Not deleted'
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time(),
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def install_nginx(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/nginx.yml"
        form = InstallNginx(data=request.POST, prefix="installedNginx")
        print "første"
        print form.errors
        if form.is_valid():
            print "andre"
            server = request.POST.getlist('nginx-servers')
            if server[0] == 'all':
                server.pop(0)
            user = request.user
            s_p = request.POST.getlist('nginx-sudo_password')[0]
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_nginx(p_o.pb_output(), items)
                instance = form.save(commit=False)
                if check:
                    exists = NginxInstallation.objects.filter(servers=items).exists()
                    if not exists:
                        instance.pk = None
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
        path = "accounts/ansibleScripts/php.yml"
        form = InstallPhp(data=request.POST, prefix="installedPhp")
        print "første"
        print form.errors
        if form.is_valid():
            print "andre"
            server = request.POST.getlist('php-servers')
            if server[0] == 'all':
                server.pop(0)
            user = request.user
            p_o = run_playbook()
            s_p = request.POST.getlist('php-sudo_password')[0]
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_php(p_o.pb_output(), items)
                print check
                instance = form.save(commit=False)
                if check:
                    exists = PhpInstallation.objects.filter(servers=items).exists()
                    print exists
                    if not exists:
                        instance.pk = None
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


def start_postgres_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/postgresql/startPostgres"
        form = InstalledPostgresForm(data=request.POST, prefix="installedPostgres")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_postgres-servers')
            s_p = request.POST.getlist('installed_postgres-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def stop_postgres_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/postgresql/stopPostgres"
        form = InstalledPostgresForm(data=request.POST, prefix="installedPostgres")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_postgres-servers')
            s_p = request.POST.getlist('installed_postgres-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
              'p_output': p_o.pb_output(),
              't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def restart_postgres_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/postgresql/restartPostgres"
        form = InstalledPostgresForm(data=request.POST, prefix="installedPostgres")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_postgres-servers')
            s_p = request.POST.getlist('installed_postgres-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
              'p_output': p_o.pb_output(),
              't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def reload_postgres_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/postgresql/reloadPostgres"
        form = InstalledPostgresForm(data=request.POST, prefix="installedPostgres")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_postgres-servers')
            s_p = request.POST.getlist('installed_postgres-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
              'p_output': p_o.pb_output(),
              't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def uninstall_postgres_db(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/postgresql/uninstallPostgres"
        form = InstalledPostgresForm(data=request.POST, prefix="installedPostgres")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_postgres-servers')
            s_p = request.POST.getlist('installed_postgres-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_db(p_o.pb_output(), items)
                if check:
                    query = DatabaseConnection.objects.filter(server_name=items, database="PostgreSql")
                    exists = query.exists()
                    print exists
                    if exists:
                        query.delete()
                        del query
                        print "Deleted"
                    else:
                        print 'Not deleted'
            context = {
              'p_output': p_o.pb_output(),
              't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def start_nginx(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/nginx/startNginx"
        form = InstalledNginxForm(data=request.POST, prefix="installedNginx")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_nginx-servers')
            s_p = request.POST.getlist('installed_nginx-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
              'p_output': p_o.pb_output(),
              't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def stop_nginx(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/nginx/stopNginx"
        form = InstalledNginxForm(data=request.POST, prefix="installedNginx")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_nginx-servers')
            s_p = request.POST.getlist('installed_nginx-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def restart_nginx(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/nginx/restartNginx"
        form = InstalledNginxForm(data=request.POST, prefix="installedNginx")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_nginx-servers')
            s_p = request.POST.getlist('installed_nginx-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def reload_nginx(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/nginx/reloadNginx"
        form = InstalledNginxForm(data=request.POST, prefix="installedNginx")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_nginx-servers')
            s_p = request.POST.getlist('installed_nginx-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def uninstall_nginx(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/nginx/uninstallNginx"
        form = InstalledNginxForm(data=request.POST, prefix="installedNginx")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_nginx-servers')
            s_p = request.POST.getlist('installed_nginx-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_nginx(p_o.pb_output(), items)
                if check:
                    query = NginxInstallation.objects.filter(servers=items)
                    exists = query.exists()
                    print exists
                    if exists:
                        query.delete()
                        del query
                        print "Deleted"
                    else:
                        print 'Not deleted'
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")


def uninstall_php(request):
    if request.method == 'POST':
        path = "accounts/ansibleScripts/modifyScripts/php/uninstallPhp"
        form = InstalledNginxForm(data=request.POST, prefix="installedPhp")
        print request.POST
        print form.errors
        if form.is_valid():
            server = request.POST.getlist('installed_php-servers')
            s_p = request.POST.getlist('installed_php-sudo_password')[0]
            user = request.user
            p_o = run_playbook()
            p_o.run_pb(user=user, s_p=s_p, server=server, path=path)
            for items in server:
                c_i = SuccessfullInstall()
                check = c_i.check_install_php(p_o.pb_output(), items)
                if check:
                    query = PhpInstallation.objects.filter(servers=items)
                    exists = query.exists()
                    print exists
                    if exists:
                        query.delete()
                        del query
                        print "Deleted"
                    else:
                        print 'Not deleted'
            context = {
                'p_output': p_o.pb_output(),
                't_output': p_o.r_time()
            }
            return JsonResponse(context, safe=False)
        else:
            print "failed"
            return HttpResponse("Error: Something went wrong")