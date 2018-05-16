# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.hashers import make_password


# class UserProfileManager(models.Manager):
#    def get_queryset(self):
#        return super(UserProfileManager, self).get_queryset().filter(city='Horten')



DATABASE_CHOICES = {
    ('MySql', 'MYSQL'),
    ('PostgreSql', 'POSTGRESQL')
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, )
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)


    #   Horten = UserProfileManager()
    #   objects = models.Manager()

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class ServerConnection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    server_nickname = models.CharField(max_length=20, unique=True, default='', help_text='Make a name for your server')
    server_ip = models.CharField(max_length=20, default='', help_text='IP: x.x.x.x')
    sudo_user = models.CharField(max_length=100, default='',
                                 help_text='Username of you servers user with root priviliges')

    def save(self, *args, **kwargs):
        super(ServerConnection, self).save(*args, **kwargs)

    def __str__(self):
        # return self.user.username
        # return self.user.username, self.server_ip
        return '{} {} {} {}'.format(self.server_ip, self.sudo_user, self.server_nickname, self.user)


class DatabaseConnection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    server_name = models.CharField(max_length=50, help_text='Choose server')
    database = models.CharField(max_length=10, choices=DATABASE_CHOICES, default='MySql', help_text='Choose database')
    database_name = models.CharField(max_length=20, help_text="Enter the name you want for you database")
    username = models.CharField(max_length=10, help_text='Enter a username for the database')
    password = models.CharField(max_length=30, help_text="Enter a password for the database user")
    sudo_password = models.CharField(max_length=30, help_text="Enter a password for the database user")

    def save(self, *args, **kwargs):
        super(DatabaseConnection, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {} {}'.format(self.server_name, self.database, self.user)


class InstalledDb(models.Model):
    servers = models.CharField(max_length=50, help_text='Choose server')


class InstalledNginx(models.Model):
    servers = models.CharField(max_length=50, help_text='Choose server')


class NginxInstallation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servers = models.CharField(max_length=50, help_text='Choose server')

    def save(self, *args, **kwargs):
        super(NginxInstallation, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.servers, self.user)


class PhpInstallation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servers = models.CharField(max_length=50, help_text='Choose server')

    def save(self, *args, **kwargs):
        super(PhpInstallation, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.servers, self.user)






