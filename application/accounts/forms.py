from django import forms

from .models import DatabaseConnection, ServerConnection, InstalledDb, NginxInstallation, PhpInstallation, InstalledNginx
from .customScripts import ServerQuery
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class ConnectToServer(forms.ModelForm):
    sudo_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ServerConnection
        fields = (
            'server_nickname',
            'server_ip',
            'sudo_user',
            'sudo_password'
        )


class CreateRemoteDatabase(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    sudo_password = forms.CharField(widget=forms.PasswordInput)
    sq = ServerQuery()
    server_name = forms.MultipleChoiceField(sq.get_server_choices, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = DatabaseConnection
        fields = (
            'server_name',
            'database',
            'database_name',
            'username',
            'password',
            'sudo_password'
            )


class InstallNginx(forms.ModelForm):
    sq = ServerQuery()
    sn = sq.get_server_choices
    servers = forms.MultipleChoiceField(sn, required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = NginxInstallation
        fields = (
            'servers',
        )


class InstallPhp(forms.ModelForm):
    sq = ServerQuery()
    sn = sq.get_server_choices
    servers = forms.MultipleChoiceField(sn, required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = PhpInstallation
        fields = (
            'servers',
        )


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )


class InstalledDatabaseForm(forms.ModelForm):
    try:
        ds = ServerQuery()
        db = ds.get_installed_db_servers()
        servers = forms.MultipleChoiceField(db, required=False, widget=forms.CheckboxSelectMultiple)
    except:
        servers = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = InstalledDb
        fields = (
            'servers',
        )


class InstalledNginxForm(forms.ModelForm):
    try:
        ds = ServerQuery()
        db = ds.get_installed_nginx()
        servers = forms.MultipleChoiceField(db, required=False, widget=forms.CheckboxSelectMultiple)
    except:
        servers = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = InstalledNginx
        fields = (
            'servers',
        )


#        exclude =