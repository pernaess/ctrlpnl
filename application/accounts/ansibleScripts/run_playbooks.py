import os
from ..customScripts import ElapsedTimeThread
import time, collections
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from datetime import datetime
from ansible.plugins.callback import CallbackBase
from ..models import ServerConnection

"""Custom ansbile run callback, overrides custom Ansible callback plugin

:param CallbackBase: Class providing Ansible callback methods
"""
class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_name = {}
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.host_skipped = {}
        self.start_time = datetime.now()
        self.run_time = ""

    def v2_runner_on_unreachable(self, result):
        self.host_name[result._host.get_name()] = result
        self.host_unreachable["{},{}".format(result.task_name, self.server_name(result))] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_name[result._host.get_name()] = result
        self.host_ok["{},{}".format(result.task_name, self.server_name(result))] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_name[result._host.get_name()] = result
        self.host_failed["{},{}".format(result.task_name, self.server_name(result))] = result

    def v2_runner_on_skipped(self, result, *args, **kwargs):
        self.host_name[result._host.get_name()] = result
        self.host_skipped["{},{}".format(result.task_name, self.server_name(result))] = result

    def _days_hours_minutes_seconds(self, runtime):
        ''' internal helper method for this callback '''
        minutes = (runtime.seconds // 60) % 60
        r_seconds = runtime.seconds - (minutes * 60)
        return runtime.days, runtime.seconds // 3600, minutes, r_seconds

    def v2_playbook_on_stats(self, stats):
        end_time = datetime.now()
        runtime = end_time - self.start_time
        self.run_time = self._days_hours_minutes_seconds(runtime)

    def server_name(self, result):
        address = result._host.get_name().split("@")
        address = address[1]
        nickname = ServerConnection.objects.values_list(
            'server_nickname', flat=True).distinct().filter(
            server_ip=address,
        )
        name = "{}".format(nickname).split("'")
        return name[1]


""" Runs Ansible Playbooks """
class run_playbook(object):

    def __init__(self, *args, **kwargs):
        self.results_raw = {}
        self.runtime = ""

    """ Runs a playbook with provided variables, filters output for smoother display
      
    :param user - Current logged in user
    :param s_p - Sudo password
    :param server - A list of server names
    :param db_user - Username for database
    :param db_pass - Password for database
    :param db_name - Name for database
    :param path - Playbook file path
    """
    def run_pb(self, user='', s_p='', server='', db_user='', db_pass='', db_name='', path=''):
        address = []

        for servers in server:
            sudoUser = ServerConnection.objects.values_list(
              'sudo_user', flat=True).distinct().filter(
              user=user, server_nickname=servers
              )
            IP = ServerConnection.objects.values_list(
              'server_ip', flat=True).distinct().filter(
              user=user, server_nickname=servers
            )
            print IP
            IP = "{0}".format(IP).split("'")
            IP = IP[1]
            sudoUser = "{0}".format(sudoUser).split("'")
            sudoUser = sudoUser[1]

            print '{0}@{1}'.format(sudoUser, IP)
            address.append('{0}@{1}'.format(sudoUser, IP))

        print address
        loader = DataLoader()
        inventory = InventoryManager(
            loader=loader,
            sources='accounts/ansibleScripts/hosts.ini'
        )
        variable_manager = VariableManager(
            loader=loader,
            inventory=inventory
        )
        playbook_path = path

        if not os.path.exists(playbook_path):
            print '[INFO] The playbook does not exist'

        Options = namedtuple(
         'Options', [
             'listtags',
             'listtasks',
             'listhosts',
             'syntax',
             'connection',
             'module_path',
             'forks',
             'remote_user',
             'private_key_file',
             'ssh_common_args',
             'ssh_extra_args',
             'sftp_extra_args',
             'scp_extra_args',
             'become',
             'become_method',
             'become_user',
             'verbosity',
             'check',
             'diff'
            ]
        )
        options = Options(
            listtags=False,
            listtasks=False,
            listhosts=False,
            syntax=False,
            connection='ssh',
            module_path=None,
            forks=100,
            remote_user=None,
            private_key_file='/home/per/.ssh/id_rsa',
            ssh_common_args=None,
            ssh_extra_args=None,
            sftp_extra_args=None,
            scp_extra_args=None,
            become=False,
            become_method=None,
            become_user='root',
            verbosity=None,
            check=False,
            diff=False
        )

        variable_manager.extra_vars = {
            'user': address,
            'ansible_become_pass': s_p,
            'db_user': db_user,
            'db_pass': db_pass,
            'db_name': db_name
        } # This can accomodate various other command line arguments.`

        passwords = {}

        pbex = PlaybookExecutor(
            playbooks=[playbook_path],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader, options=options,
            passwords=passwords
        )
        callback = ResultsCollector()
        pbex._tqm._stdout_callback = callback
        start=time.time()
        thread = ElapsedTimeThread()
        thread.start()
        pbex.run()
        thread.stop()
        thread.join()
        print ''
        print("Finished in {:.3f} seconds".format(time.time() - start))

        for result in callback.host_name:
            print result + ' testing output of server hst in callback'
        # Pulling results from their respective dictionaries.
        self.result_puller(callback.host_unreachable.items(), 'Unreachable')
        self.result_puller(callback.host_ok.items(), 'Success')
        self.result_puller(callback.host_failed.items(), 'Failed')
        self.result_puller(callback.host_skipped.items(), 'Skipped')

        print self.results_raw
        self.runtime = callback.run_time
        print self.runtime

    def result_puller(self, item_dict, format_string):
        for host, result in item_dict:
            host = '{}'.format(host)
            if 'add_host' not in host:
                self.results_raw[host] = ('{}'.format(format_string))

    """ Returns the class dict 'resuls_raw """
    def pb_output(self):
        output = collections.OrderedDict(sorted(self.results_raw.items(), key=lambda x: x[0].split(",")[1]))
        return output

    """ Returns the overall process time of an ansible playbook """
    def r_time(self):
        seconds = self.runtime[3]
        minutes = self.runtime[2]
        process = "Process took {}m : {}s".format(minutes, seconds)
        return process
















