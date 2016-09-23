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
import string
from urllib.parse import urlparse, urlunparse

from ..base import Transfer
from ...util import calculate_file_checksum


label = "MD5 Checksum"


logger = logging.getLogger("bdss")


def can_attempt_verification(transfer, output_path):
    return True


def _md5_checksum_url(data_file_url):
    p = urlparse(data_file_url)
    return urlunparse((p.scheme, p.netloc, p.path + ".md5", p.params, p.query, p.fragment))


def _get_checksum(checksum_url, mechanism_name, mechanism_options, data_source_id=None):
    checksum_transfer = Transfer(checksum_url,
                                 mechanism_name,
                                 mechanism_options,
                                 data_source_id=data_source_id)

    checksum_data = checksum_transfer.get_data(display_output=False)
    return checksum_data.decode().strip().lower()


def _validate_md5_checksum(possible_checksum):
    """
    Validate that a string matches the format of an MD5 checksum (32 characters, hex digits)
    """
    return len(possible_checksum) == 32 and all(c in string.hexdigits for c in possible_checksum)


def verify_transfer(transfer, output_path):
    checksum_url = _md5_checksum_url(transfer.url)

    logger.debug("Fetching MD5 checksum from %s" % checksum_url)

    correct_checksum = _get_checksum(checksum_url,
                                     transfer.mechanism_name,
                                     transfer.mechanism_options,
                                     transfer.data_source_id)

    if not _validate_md5_checksum(correct_checksum):
        raise ValueError("Fetched value is not a valid MD5 checksum")

    logger.info("Correct MD5 checksum = %s" % correct_checksum)
    logger.debug("Calculating MD5 checksum...")
    actual_checksum = calculate_file_checksum("md5", output_path)
    logger.info("MD5 Checksum = %s" % actual_checksum)
    return actual_checksum == correct_checksum
