# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .forms import CreateRemoteDatabase


from django.shortcuts import render, redirect
from accounts.forms import (
     RegistrationForm,
     EditProfileForm,
     CreateRemoteDatabase
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'accounts/home.html')


# Handles forms in services.html based on form submitted
def services(request):
    if request.method == 'POST':
        if 'create_db' in request.POST:
            createdbform = CreateRemoteDatabase(request.POST, prefix='createDB')
            if createdbform.is_valid():
                createdbform.save()
                return redirect('accounts:home')
    else:
        createdbform = CreateRemoteDatabase(prefix='createDB')
        args = {'form': createdbform}

    return render(request, 'accounts/services.html', args)


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




