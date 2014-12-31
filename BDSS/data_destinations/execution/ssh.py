import socket

from paramiko.ssh_exception import AuthenticationException
from paramiko.rsakey import RSAKey
from StringIO import StringIO
from . import BaseExecutionMethod, JobExecutionError
from ..util import SSHClient

class SshExecutionMethod(BaseExecutionMethod):

    requires_ssh_key = True

    def __init__(self, destination_host, **kwargs):
        self.command = "for f in urls/group*.txt; do nohup python ./scripts/transfer.py $f & done"
        super(SshExecutionMethod, self).__init__(destination_host, **kwargs)

    def connect(self):
        self._ssh = SSHClient()
        try:
            self._ssh.connect(self.destination_host, 22, self.user, None, RSAKey.from_private_key(StringIO(self.key)), None, None, True, False)
        except AuthenticationException:
            raise JobExecutionError('SSH unable to authenticate with destination')
        except socket.error:
            raise JobExecutionError('SSH unable to connect to destination')

    def execute_job(self, working_directory):
        self._ssh.exec_sync_command('cd "%s"; %s' % (working_directory, self.command))

    def disconnect(self):
        self._ssh.close()
