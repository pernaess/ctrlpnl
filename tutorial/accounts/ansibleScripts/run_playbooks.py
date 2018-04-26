import os

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from datetime import datetime
from ansible.plugins.callback import CallbackBase
from ..models import ServerConnection


# Custom made callback class for gathering information on
# Ansible plays. Overrides the default Ansible callback plugin
class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.host_skipped = {}
        self.start_time = datetime.now()
        self.run_time = ""

    def v2_runner_on_unreachable(self, result):
        #self.host_unreachable[result._host.get_name()] = result
        self.host_unreachable[result.task_name] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        #self.host_ok[result._host.get_name()] = result
        self.host_ok[result.task_name] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        #self.host_failed[result._host.get_name()] = result
        self.host_failed[result.task_name] = result

    def v2_runner_on_skipped(self, result, *args, **kwargs):
        #self.host_failed[result._host.get_name()] = result
        self.host_skipped[result.task_name] = result

    def _days_hours_minutes_seconds(self, runtime):
        ''' internal helper method for this callback '''
        minutes = (runtime.seconds // 60) % 60
        r_seconds = runtime.seconds - (minutes * 60)
        return runtime.days, runtime.seconds // 3600, minutes, r_seconds

    def v2_playbook_on_stats(self, stats):
        end_time = datetime.now()
        runtime = end_time - self.start_time
        self.run_time = self._days_hours_minutes_seconds(runtime)


# Runs ansible playbooks
class run_playbook(object):

  def __init__(self, *args, **kwargs):
      self.results_raw = {}
      self.runtime = ""

    # Runs a playbook with provided variables
    # and filters gathered play information for a smoother display.
  def run_pb(self, user, s_p, server, db_user, db_pass, db_name):

      sudoUser = ServerConnection.objects.values_list(
        'sudo_user', flat=True).distinct().filter(
        user=user, server_nickname=server
        )
      IP = ServerConnection.objects.values_list(
        'server_ip', flat=True).distinct().filter(
        user=user, server_nickname=server
      )

      IP = "{0}".format(IP).split("'")
      IP = IP[1]
      sudoUser = "{0}".format(sudoUser).split("'")
      sudoUser = sudoUser[1]

      print '{0}@{1}'.format(sudoUser, IP)

      loader = DataLoader()

      inventory = InventoryManager(
          loader=loader,
          sources='accounts/ansibleScripts/hosts.ini'
      )
      variable_manager = VariableManager(
          loader=loader,
          inventory=inventory
      )
      playbook_path = 'accounts/ansibleScripts/mysql.yml'

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

      user = '{0}@{1}'.format(sudoUser, IP)
      variable_manager.extra_vars = {
          'user': user,
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
      pbex.run()

      # # Pulling results from their respective dictionaries.
      self.result_puller(callback.host_ok.items(), 'Success')
      self.result_puller(callback.host_failed.items(), 'Failed')
      self.result_puller(callback.host_unreachable.items(), 'Unreachable')
      self.result_puller(callback.host_skipped.items(), 'Skipped')

      print self.results_raw
      self.runtime = callback.run_time
      print self.runtime

  def result_puller(self, item_dict, format_string):
      for host, result in item_dict:
          host = '{}'.format(host)
          if host != 'add_host':
              self.results_raw[host] = ('{}'.format(format_string))


  # Returns the class dictionary 'results_raw'.
  def pb_output(self):
    return self.results_raw

  #Returns the overall process time of an ansible playbook
  def r_time(self):
    seconds = self.runtime[3]
    minutes = self.runtime[2]
    process = "Process took {}m : {}s".format(minutes, seconds)
    return process














