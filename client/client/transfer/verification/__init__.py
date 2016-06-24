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

import logging
import traceback

from . import md5_checksum_verification
from . import sra_toolkit_vdb_validate_verification


logger = logging.getLogger("bdss")


verification_methods = [
    md5_checksum_verification,
    sra_toolkit_vdb_validate_verification
]


class VerificationReport():
    """
    Describes the results of file verification

    method - String - Name of verification method
    result - Boolean? - Result of verification method. True if verified, False if failed, None if unknown
    """

    def __init__(self, method=None, result=None):
        self.method = method
        self.result = result

    def __str__(self):
        display_result = {
            True: "verified",
            False: "failed",
            None: "unknown"
        }
        return "%s -> %s" % (self.method, display_result[self.result])


def verify_data_transfer(transfer, output_path):
    """
    Attempt to verify a downloaded file using all available methods.

    Parameters:
    url - String - The URL the data file was transferred from.
    output_path - String - The path to the transferred data file.

    Returns:
    VerificationReport[]
    """
    logger.info("Verifying transfer from %s" % transfer.url)

    reports = []
    for method in verification_methods:

        if not method.can_attempt_verification(transfer, output_path):
            logger.debug("Skipping verification with %s" % method.label)
            continue

        report = VerificationReport(method=method.label, result=None)

        try:
            report.result = method.verify_transfer(transfer, output_path)
            if report.result:
                logger.info("Verified with %s" % method.label)
            else:
                logger.error("Failed verification by %s" % method.label)

        except:
            logger.warn("Unable to verify with %s" % method.label)
            logger.debug(traceback.format_exc())

        reports.append(report)

    return reports
