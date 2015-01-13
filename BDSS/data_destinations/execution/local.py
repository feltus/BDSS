import subprocess

from . import BaseExecutionMethod

## Execute a data transfer job on the local machine.
class LocalExecutionMethod(BaseExecutionMethod):

    def __init__(self, destination_host, **kwargs):
        self.command = "for f in urls/group*.txt; do python ./scripts/transfer.py $f; done"
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

    def execute_job(self, working_directory):
        subprocess.Popen(
            self.command,
            cwd=working_directory,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    def disconnect(self):
        pass
