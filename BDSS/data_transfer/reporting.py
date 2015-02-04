import json
import Queue
import sys

## Class to report URL transfer and job statuses to BDSS server.
class JobStatusReporter(object):

    ##
    #  @param multiprocessing.Queue report_queue
    def __init__(self, report_queue):
        self._report_queue = report_queue

    ## Clone this object.
    #  @return A new reporter with the same configuration as this one.
    def clone(self):
        return self.__class__(self._report_queue)

    ## Send report data to server.
    #
    #  @param dict data The data to send.
    #
    def _report(self, data):
        sent = False
        while not sent:
            try:
                self._report_queue.put(data, True, 5.0)
                sent = True
            except Queue.Full:
                pass

    ## Report that the transfer of a data URL has started.
    #
    #  @param string data_url The URL whose transfer has started.
    #  @param int time_started The time at which the transfer started.
    #
    def report_transfer_started(self, data_url, time_started):
        self._report({
            'status': 'started',
            'url': data_url,
            'current_time': time_started
        })

    ## Report that the transfer of a data URL has succesfully finished.
    #
    #  @param string data_url The URL whose transfer has finished.
    #  @param int time_finished The time at which the transfer finished.
    #  @param float measured_time Measured time (in seconds) required for the transfer.
    #  @param int file_size Size of the downloaded file (in bytes).
    #
    def report_transfer_finished(self, data_url, time_finished, measured_time, file_size):
        self._report({
            'status': 'finished',
            'url': data_url,
            'current_time': time_finished,
            'transfer_size': file_size,
            'measured_transfer_time': measured_time
        })

    ## Report that the transfer of a data URL has failed.
    #
    #  @param string data_url The URL whose transfer failed.
    #  @param int time_started The time at which the transfer failed.
    #  @param float measured_time Measured time (in seconds) before the transfer failed.
    #  @param string error_message Error message to display to the job's owner.
    #
    def report_transfer_failed(self, data_url, time_finished, measured_time, error_message):
        self._report({
            'status': 'finished',
            'error': error_message,
            'url': data_url,
            'current_time': time_finished,
            'measured_transfer_time': measured_time
        })
