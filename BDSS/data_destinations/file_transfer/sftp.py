import socket

from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException
from StringIO import StringIO
from . import BaseFileTransferMethod, FileTransferError
from ..util import SSHClient

## Transfer job files to the destination via Sftp.
class SftpFileTransferMethod(BaseFileTransferMethod):

    requires_ssh_key = True

    def connect(self):
        self._ssh = SSHClient()
        try:
            self._ssh.connect(self.destination_host, 22, self.user, None, RSAKey.from_private_key(StringIO(self.key)), None, None, True, False)
            self._sftp = self._ssh.open_sftp()
        except AuthenticationException:
            raise FileTransferError('SSH unable to authenticate with destination')
        except socket.error:
            raise FileTransferError('SSH unable to connect to destination')
        except IOError:
            raise FileTransferError('Unable to write files')

    def mkdir_p(self, dir_path):
        self._ssh.exec_sync_command('mkdir -p "%s"' % dir_path)

    def transfer_file(self, dest_file_path, file_data):
        remote_file = self._sftp.open(dest_file_path, 'w')
        remote_file.write(file_data)
        remote_file.close()

    def disconnect(self):
        self._sftp.close()
        self._ssh.close()
