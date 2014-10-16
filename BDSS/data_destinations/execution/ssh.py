from . import BaseExecutionMethod
from ..util import SSHClient

class SshExecutionMethod(BaseExecutionMethod):

    def __init__(self, **kwargs):
        self.command = "for f in urls/group*.txt; do nohup python ./scripts/transfer.py $f &; done"
        super(SshExecutionMethod, self).__init__(**kwargs)

    def connect(self):
        self._ssh = SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.connect(self.host, 22, self.user, self.password, None, None, None, True, False)

    def execute_job(self, working_directory):
        self._ssh.exec_sync_command('cd "%s"; %s' % (working_directory, self.command))

    def disconnect(self):
        self._ssh.close()
