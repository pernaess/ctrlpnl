import os
import platform
import threading, time
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

    def check_install(self, output, server):
        check = 'Install database server,{}'.format(server)
        if check in output:
            if output[check] == 'Success':
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


class ElapsedTimeThread(threading.Thread):
    """"Stoppable thread that prints the time elapsed"""
    def __init__(self):
        super(ElapsedTimeThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        thread_start = time.time()
        while not self.stopped():
            print("\rElapsed Time {:.0f} seconds".format(time.time()-thread_start))
            time.sleep(1)


