import subprocess
import time

from . import BaseTransferMethod

class SequentialCurlTransferMethod(BaseTransferMethod):

    def transfer_data(self, data_urls):
        for url in data_urls:

            self.report_transfer_started(url, time.time())
            error_msg = None
            start_time = time.time()
            try:
                subprocess.check_output("curl --output \"%s\" \"%s\"" % (self.output_path(url), url), stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                error_msg = e.output
            finally:
                elapsed_time = time.time() - start_time
                self.report_transfer_finished(url, time.time(), elapsed_time, error_msg)
