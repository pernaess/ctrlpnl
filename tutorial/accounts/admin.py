# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserProfile, ServerConnection, DatabaseConnection


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'website', 'city', 'phone')

    def user_info(self, obj):
        return obj.description

# Overwrite sorting
    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone', 'user')
        return queryset


class UserServerConnection(admin.ModelAdmin):
    list_display = ('user', 'server_nickname', 'server_ip', 'sudo_user')

    def server_connection(self, obj):
        return obj.description


class UserDatabaseConnection(admin.ModelAdmin):
    list_display = ('user', 'server_name', 'database')

    def server_connection(self, obj):
        return obj.description


# Shorten names example:
# user_info.short_description = 'Info'

# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ServerConnection, UserServerConnection)
admin.site.register(DatabaseConnection, UserDatabaseConnection)


