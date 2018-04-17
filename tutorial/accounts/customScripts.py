import os
import platform


def server_status(ip_list):

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

