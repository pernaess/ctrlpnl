from django.conf.urls import url
from ctrlpnl import views

urlpatterns= [
    url(r'^$', views.ctrlpnl, name='ctrlpnl')
]