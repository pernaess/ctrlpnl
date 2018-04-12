# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from .models import ServerConnection
from django.shortcuts import render, redirect
from .forms import (
     RegistrationForm,
     EditProfileForm,
     CreateRemoteDatabase,
     ConnectToServer
)

from .ansibleScripts.run_playbooks import run_mysql

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


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
            if createdbform.is_valid():
                print createdbform.cleaned_data['username']
                run_mysql(createdbform.cleaned_data['password'])
                return redirect('accounts:ServicesView')
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