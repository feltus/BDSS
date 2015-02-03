import json
import sys
import urllib2

## Class to report URL transfer and job statuses to BDSS server.
class JobStatusReporter(object):

    ##
    #  @param string server_url The root URL of the BDSS server.
    #  @param int job_id The ID of the job to report statuses for.
    #  @param string reporting_token A token to use for authorization to the server.
    #
    def __init__(self, server_url, job_id, reporting_token):
        self.server_url = server_url
        self.job_id = job_id
        self.reporting_token = reporting_token

    ## Clone this object.
    #
    #  @return A new reporter with the same configuration as this one.
    #
    def clone(self):
        return self.__class__(self.server_url, self.job_id, self.reporting_token)

    ## The URL to send reports for this job to.
    #
    #  @return string
    #
    def report_url(self):
        return self.server_url + '/jobs/' + str(self.job_id)

    ## Send data to URL. Use reporting token for authorization.
    #
    #  @param string url The URL to post data to.
    #  @param dict data The data to post.
    #
    #  @return string The response from the server.
    #
    def _report(self, url, data):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token ' + self.reporting_token
        }
        request = urllib2.Request(url, json.dumps(data), headers)
        try:
            f = urllib2.urlopen(request)
            response = f.read()
            f.close()
            return response
        except urllib2.HTTPError as e:
            print >> sys.stderr, 'Failed to report status: ' + json.dumps(data)

    ## Report that the transfer of a data URL has started.
    #
    #  @param string data_url The URL whose transfer has started.
    #  @param int time_started The time at which the transfer started.
    #
    #  @return string The response from the server.
    #
    def report_transfer_started(self, data_url, time_started):
        return self._report(self.report_url() + '/status', {
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
    #  @return string The response from the server.
    #
    def report_transfer_finished(self, data_url, time_finished, measured_time, file_size):
        return self._report(self.report_url() + '/status', {
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
    #  @return string The response from the server.
    #
    def report_transfer_failed(self, data_url, time_finished, measured_time, error_message):
        return self._report(self.report_url() + '/status', {
            'status': 'finished',
            'error': error_message,
            'url': data_url,
            'current_time': time_finished,
            'measured_transfer_time': measured_time
        })
