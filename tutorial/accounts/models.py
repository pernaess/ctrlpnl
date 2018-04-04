# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# class UserProfileManager(models.Manager):
#    def get_queryset(self):
#        return super(UserProfileManager, self).get_queryset().filter(city='Horten')

DATABASE_CHOICES = {
    ('MySql', 'MYSQL'),
    ('SqlLite', 'SQLLITE'),
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


class DatabaseConnection(models.Model):
    database = models.CharField(max_length=10, choices=DATABASE_CHOICES, default='MySql')
    database_name = models.CharField(max_length=20, help_text="YOYOYOYO")
    username = models.CharField(max_length=10, help_text="hhhh")
    password = models.CharField(max_length=30, help_text="ooooo")


class ServerConnection(models.Model):
    server_ip = models.CharField(max_length=20, help_text='IP: x.x.x.x')
    ssh_key = models.CharField(max_length=100, help_text='Post key')






