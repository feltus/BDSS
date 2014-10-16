import subprocess

from . import BaseExecutionMethod

## Execute a data transfer job on the local machine.
class LocalExecutionMethod(BaseExecutionMethod):

    def __init__(self, **kwargs):
        self.command = "for f in urls/group*.txt; do python ./scripts/transfer.py $f; done"
        super(LocalExecutionMethod, self).__init__(**kwargs)

    def connect(self):
        pass

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
