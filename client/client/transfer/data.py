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
import os
import time

from .reporting import TransferReport
from .verification import verify_data_transfer
from ..util import calculate_file_checksum


logger = logging.getLogger("bdss")


def run_data_transfer(transfer, output_path):
    """
    Transfer a data file and generate report.

    Parameters:
    transfer - Transfer - Data file Transfer.
    output_path - String - The path to save the downloaded file to.

    Returns:
    TransferReport - Report describing result of transfer.
    """
    logger.debug("Data file transfer")
    logger.debug(transfer)

    report = TransferReport()
    report.url = transfer.url
    report.mechanism_name = transfer.mechanism_name
    report.mechanism_options = transfer.mechanism_options
    report.success = False

    start_time = time.time()

    try:
        (report.success, report.mechanism_output) = transfer.run(output_path)
    except Exception:
        logger.exception("Exception in transfer mechanism")
    finally:
        report.duration = time.time() - start_time

        report.file_size = 0
        report.checksum = None

        if os.path.isfile(output_path):
            report.size = os.stat(output_path).st_size
            report.checksum = calculate_file_checksum("md5", output_path)

        if report.success:
            logger.info("Success. Transferred %d bytes in %d seconds", report.size, report.duration)
            report.verification = verify_data_transfer(transfer, output_path)
        else:
            logger.warn("Unable to transfer file")

    return report
