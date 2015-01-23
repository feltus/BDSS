import subprocess
import time

from . import BaseTransferMethod, output_path, get_downloaded_file_size

class SequentialWgetTransferMethod(BaseTransferMethod):

    def transfer_data(self, data_urls):
        for url in data_urls:

            self.reporter.report_transfer_started(url, time.time())
            error_msg = None
            start_time = time.time()
            try:
                subprocess.check_output("wget --output-document=\"%s\" \"%s\"" % (output_path(url), url), stderr=subprocess.STDOUT, shell=True)
                elapsed_time = time.time() - start_time
                self.reporter.report_transfer_finished(url, time.time(), elapsed_time, get_downloaded_file_size(url)))
            except subprocess.CalledProcessError as e:
                elapsed_time = time.time() - start_time
                error_msg = e.output
                self.reporter.report_transfer_failed(url, time.time(), elapsed_time, error_msg)
