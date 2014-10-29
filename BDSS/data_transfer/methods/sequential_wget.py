import subprocess
import time

from . import BaseTransferMethod

class SequentialWgetTransferMethod(BaseTransferMethod):

    def transfer_data(self, data_urls):
        for url in data_urls:

            self.report_transfer_started(url, time.time())
            error_msg = None
            start_time = time.time()
            try:
                subprocess.check_output("wget --output-document=\"%s\" \"%s\"" % (self.output_path(url), url), stderr=subprocess.STDOUT, shell=True)
                elapsed_time = time.time() - start_time
                self.report_transfer_finished(url, time.time(), elapsed_time)
            except subprocess.CalledProcessError as e:
                elapsed_time = time.time() - start_time
                error_msg = e.output
                self.report_transfer_failed(url, time.time(), elapsed_time, error_msg)
