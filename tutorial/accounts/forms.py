from django import forms

from .models import DatabaseConnection, ServerConnection, AjaxTest
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


class CreateRemoteDatabase(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    sudo_password = forms.CharField(widget=forms.PasswordInput)
    squery = ServerConnection.objects.order_by('server_nickname').values_list('server_nickname', flat=True).distinct()
    squery.choices = [('', 'None')] + [(id, id) for id in squery]
    server_name = forms.ChoiceField(squery.choices, widget=forms.Select())

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


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )


class ConnectToServer(forms.ModelForm):
    sudo_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ServerConnection
        fields = (
            'server_nickname',
            'server_ip',
            'sudo_user',
        )


class ajaxForm(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = AjaxTest
        fields = (
          'name',
        )


class ConnCheck(forms.Form):
    hidden = forms.CharField(widget=forms.HiddenInput(), required=False)
    low = forms.CharField(required=False)





#        exclude =