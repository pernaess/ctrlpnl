from django.conf.urls import url
from ctrlpnl.views import CtrlpnlView

urlpatterns= [
    url(r'^$', CtrlpnlView.as_view(), name='ctrlpnl')
]