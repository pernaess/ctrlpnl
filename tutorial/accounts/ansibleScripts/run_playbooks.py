import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor


def run_mysql(sudo_pass):
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

    variable_manager.extra_vars = {
        'hosts': 'webserver',
        'ansible_become_pass': sudo_pass
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