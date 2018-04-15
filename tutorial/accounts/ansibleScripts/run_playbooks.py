import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ..models import ServerConnection


#
def run_mysql(user, s_p, server, db_user, db_pass, db_name):

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
        remote_user='per',
        private_key_file='/home/per/.ssh/id_rsa',
        ssh_common_args=None,
        ssh_extra_args=None,
        sftp_extra_args=None,
        scp_extra_args=None,
        become=True,
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

    results = pbex.run()
