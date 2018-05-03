import os
import platform
from .models import DatabaseConnection, ServerConnection


class Server_ping(object):

    def __init__(self, *args, **kwargs):
        self.list = []

    def server_status(self, ip_list):
        self.list = ip_list
        status_list = []
        for item in ip_list:
            if platform.system() == "Windows":
                response = os.system("ping " + item + " -n 1")
            else:
                response = os.system("ping -c 1 " + item)

            if response == 0:
                status_list.append('Running')
                print item, 'is up!'
            else:
                status_list.append("Can't connect")
                print item, 'is down!'

        return status_list


class SuccessfullInstall:

    def __init__(self, *args, **kwargs):
        self.list = []

    def check_install(self, output):
        if 'Install database server' in output:
            if output['Install database server'] == 'Success':
                return True
            else:
                return False


class ServerQuery:

    def __init__(self, *args, **kwargs):
        self.list = []

    def get_server_choices(self):
        squery = ServerConnection.objects.order_by(
            'server_nickname').values_list('server_nickname', flat=True).distinct()
        squery.choices = [('all', 'Choose all')] + [(id, id) for id in squery]
        return squery.choices



