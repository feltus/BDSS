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


logger = logging.getLogger("bdss")


verification_methods = [
    md5_checksum_verification
]


def verify_transfer(transfer_spec, output_path):
    """
    Attempt to verify a downloaded file using all available methods.
    """
    verification_results = []
    logger.info("Verifying download from %s" % transfer_spec.url)
    for method in verification_methods:
        if not method.can_attempt_verification(transfer_spec, output_path):
            logger.debug("Skipping verification with %s" % method.label)
            continue

        try:
            verified = method.verify_transfer(transfer_spec, output_path)
            if verified:
                logger.info("Verified with %s" % method.label)
            else:
                logger.error("Failed verification by %s" % method.label)
            verification_results.append(verified)
        except Exception:
            logger.warn("Unable to verify with %s" % method.label)
            logger.warn(traceback.format_exc())
            verification_results.append(None)

    if [r for r in verification_results if r is False]:
        return False
    else:
        return True
