import Queue
import subprocess
import threading
import time

from . import BaseTransferMethod, output_path, get_downloaded_file_size

class Worker(threading.Thread):

    def __init__(self, index, reporter, url_queue):
        super(Worker, self).__init__()
        self.index = index
        self.reporter = reporter
        self.url_queue = url_queue

    def run(self):
        while True:
            try:
                url = self.url_queue.get(timeout=5.0)
                print "Thread %d downloading %s to %s" % (self.index, url, output_path(url))

                self.reporter.report_transfer_started(url, time.time())
                error_msg = None
                start_time = time.time()
                try:
                    subprocess.check_output("curl --output \"%s\" \"%s\"" % (output_path(url), url), stderr=subprocess.STDOUT, shell=True)
                    elapsed_time = time.time() - start_time
                    print "Done after %fs" % elapsed_time
                    self.reporter.report_transfer_finished(url, time.time(), elapsed_time, get_downloaded_file_size(url))
                except subprocess.CalledProcessError as e:
                    elapsed_time = time.time() - start_time
                    error_msg = e.output
                    print "Failed after %fs" % elapsed_time
                    print error_msg
                    self.reporter.report_transfer_failed(url, time.time(), elapsed_time, error_msg)

                self.url_queue.task_done()

            except Queue.Empty:
                break

class ParallelCurlTransferMethod(BaseTransferMethod):

    def transfer_data(self, reporter, data_urls):

        # Queue data URLS.
        q = Queue.Queue()
        for url in data_urls:
            q.put(url)

        # Start worker threads.
        workers = []
        for i in range(0, int(self.num_streams)):
            w = Worker(i, reporter.clone(), q)
            workers.append(w)
            w.start()

        # Wait for all tasks to complete.
        q.join()
        for w in workers:
            w.join()
