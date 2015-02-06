import os
import subprocess

from . import BaseExecutionMethod

## Execute a data transfer job on the local machine.
class LocalExecutionMethod(BaseExecutionMethod):

    def __init__(self, destination_host, **kwargs):
        self.command = "python ./scripts/transfer.py {group}"
        super(LocalExecutionMethod, self).__init__(destination_host, **kwargs)

    def connect(self):
        pass

    def test_connection(self, app_url):
        response_code = None
        try:
            response_code = int(subprocess.check_output("curl -s -o /dev/null -w \"%%{http_code}\" \"%s\"" % app_url, shell=True))
        except subprocess.CalledProcessError as e:
            response_code = int(e.output)
        return 200 <= response_code < 400

    def execute_job(self, working_directory, num_processes):
        for i in xrange(0, num_processes):
            subprocess.Popen(
                self.command.format(group=i),
                cwd=os.path.expandvars(os.path.expanduser(working_directory)),
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

    def disconnect(self):
        pass
