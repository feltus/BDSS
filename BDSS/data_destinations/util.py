import time

from paramiko import SSHClient as ParamikoSSHClient
from socket import timeout

## Add method for running synchronous commands to Paramiko's SSH client.
class SSHClient(ParamikoSSHClient):

    ## Execute a command on the remote host, but block until it finishes
    #  or until the given timeout expires.
    #  @param command The command to run
    #  @param timeout Timeout in seconds
    def exec_sync_command(self, command, timeout=10.0):
        start = time.time()
        stdin, stdout, stderr = self.exec_command(command)
        i = 0
        while not stdout.channel.exit_status_ready():
            time.sleep(0.05)
            i += 1
            if i % 10 == 0 and time.time() - start > timeout:
                raise timeout('Command \'%s\' timed out after %fs' % (command, timeout))

        return (stdin, stdout, stderr)
