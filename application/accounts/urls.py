from django.conf.urls import url
from . import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete,
)

urlpatterns = [

    url(r'^$',
        login, {
            'template_name': 'accounts/home.html'
        },
        name='home'),

    url(r'^login/$',
        login, {
            'template_name': 'accounts/login.html'
        },
        name='login'),

    url(r'^logout/$',
        logout, {
            'template_name': 'accounts/logout.html'
        },
        name='logout'),

    url(r'^register/$',
        views.register,
        name='register'),

    url(r'^profile/$',
        views.view_profile,
        name='view_profile'),

    url(r'^profile/edit$',
        views.edit_profile,
        name='edit_profile'),

    url(r'^change-password/$',
        views.change_password,
        name='change_password'),

    url(r'^reset-password/$',
        password_reset, {
            'template_name': 'accounts/reset_password.html',
            'post_reset_redirect': 'accounts:password_reset_done',
            'email_template_name': 'accounts/reset_password_email.html'
        },
        name='reset_password'),

    url(r'^reset-password/done/$',
        password_reset_done, {
            'template_name': 'accounts/reset_password_done.html',
        },
        name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$',
        password_reset_confirm, {
            'template_name': 'accounts/reset_password_confirm.html',
            'post_reset_redirect': 'accounts:password_reset_complete'
        },
        name='password_reset_confirm'),

    url(r'^reset-password/complete/$',
        password_reset_complete, {
            'template_name': 'accounts/reset_password_complete.html',
        },
        name='password_reset_complete'),

    url(r'^services/$',
        views.ServicesView,
        name='ServicesView'),

    url(r'^about/$',
        views.aboutView,
        name='aboutView'),

    url(r'^dashboard/$',
        views.dashboardView,
        name='dashboardView'),

    url(r'^dashboard/CheckConn/$',
        views.CheckConn,
        name='CheckConn'),

    url(r'^services/createDB/$',
        views.createDBView,
        name='createDBView'),

    url(r'^dashboard/startDb/$',
        views.start_mysql_db,
        name='start_mysql_db'),

    url(r'^dashboard/stopDb/$',
        views.stop_mysql_db,
        name='stop_mysql_db'),

    url(r'^services/installNginx/$',
        views.install_nginx,
        name='install_nginx'),

    url(r'^services/installPHP/$',
        views.install_php,
        name='install_php'),

    url(r'^dashboard/restartMysql/$',
        views.restart_mysql_db,
        name='restart_mysql_db'),

    url(r'^dashboard/uninstallMysql/$',
        views.uninstall_mysql_db,
        name='uninstall_mysql_db'),

    url(r'^dashboard/startPostgreSql/$',
        views.start_postgres_db,
        name='start_postgres_db'),

    url(r'^dashboard/stopPostgreSql/$',
        views.stop_postgres_db,
        name='stop_postgres_db'),

    url(r'^dashboard/restartPostgreSql/$',
        views.restart_postgres_db,
        name='restart_postgres_db'),

    url(r'^dashboard/reloadPostgreSql/$',
        views.reload_postgres_db,
        name='reload_postgres_db'),

    url(r'^dashboard/uninstallPostgreSql/$',
        views.uninstall_postgres_db,
        name='uninstall_postgres_db'),

    url(r'^dashboard/startNginx/$',
        views.start_nginx,
        name='start_nginx'),

    url(r'^dashboard/stopNginx/$',
        views.stop_nginx,
        name='stop_nginx'),

    url(r'^dashboard/restartNginx/$',
        views.restart_nginx,
        name='restart_nginx'),

    url(r'^dashboard/reloadNginx/$',
        views.reload_nginx,
        name='reload_nginx'),

    url(r'^dashboard/uninstallNginx/$',
        views.uninstall_nginx,
        name='uninstall_nginx'),

    url(r'^dashboard/uninstallPhp/$',
        views.uninstall_php,
        name='uninstall_php'),
]
