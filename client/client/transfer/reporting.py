# Big Data Smart Socket
# Copyright (C) 2016 Clemson University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import requests
import textwrap

from .mechanisms import default_mechanism
from ..config import client_destination, metadata_repository_url, dtn_host, dtn_path, dtn_user


class TransferReport():
    """
    Describes the result of a transfer

    url - String - The actual URL of the transferred file
    size - Integer - The size of the transferred file in bytes
    duration - Float - The duration of the transfer in seconds
    success - Boolean - Whether the transfer succeeded or failed
    mechanism_name - String
    mechanism_options - Dictionary
    mechanism_output - String - Output of the transfer mechanism
    checksum - String - MD5 checksum of the transferred file
    verification - VerificationReport[] - If transfer succeeded, results of verification
    """

    def __init__(self, url=None,
                 size=0, duration=0, success=False,
                 mechanism_name=None, mechanism_options=None, mechanism_output=None,
                 checksum=None, verification=None):
        self.url = url
        self.size = size
        self.duration = duration
        self.success = success

        self.mechanism_name = mechanism_name
        self.mechanism_options = mechanism_options
        if not self.mechanism_name:
            (self.mechanism_name, self.mechanism_options) = default_mechanism(url)

        self.mechanism_output = mechanism_output
        self.checksum = checksum
        self.verification = verification

    def __str__(self):
        return textwrap.dedent("""\
                TransferReport:
                URL = %s
                mechanism = %s
                %s
                transfer %s
                file size = %d bytes
                duration = %f seconds
                checksum = %s
                verification:
                %s
                """ % (
            self.url,
            self.mechanism_name,
            "\n".join(["   %s: %s" % (k, v) for k, v in self.mechanism_options.items()]) if self.mechanism_options else "   No options",
            "succeeded" if self.success else "failed",
            self.size,
            self.duration,
            self.checksum,
            "\n".join(["   %s" % v for v in self.verification])))


def send_report(report):
    """
    Send a report to the metadata repository.

    Parameters:
    report - TransferReport
    """

    report_data = dict(
        url=report.url,
        file_size_bytes=report.size,
        transfer_duration_seconds=report.duration,
        is_success=report.success,
        mechanism_output=report.mechanism_output,
        file_checksum=report.checksum
    )

    if client_destination:
        report_data["destination"] = client_destination

    requests.post(metadata_repository_url + "/transfer_reports", data=report_data)


class ReportsFile():

    def __init__(self, file_handle):
        self._file = file_handle
        self._headers_written = False

    def _write_headers(self):
        self._file.write("URL,Transfer Time (s),Transfer Size (bytes),Transfer Rate(bytes/s)\n")
        self._headers_written = True

    def write_report(self, report):
        if not self._headers_written:
            self._write_headers()

        self._file.write("%s,%f,%d,%f\n" % (report.url, report.duration, report.size, report.size / report.duration))
