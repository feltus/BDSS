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
import subprocess

from ...util import is_program_on_path


label = "SRA Toolkit's vdb-validate"


logger = logging.getLogger("bdss")


def can_attempt_verification(transfer_spec, output_path):
    """
    Only attempt to verify SRA files.
    """
    _, ext = os.path.splitext(output_path)
    return ext == ".sra" and is_program_on_path("vdb-validate")


def verify_transfer(transfer_spec, output_path):
    try:
        subprocess.check_output(["vdb-validate", output_path])
        return True
    except subprocess.CalledProcessError:
        return False
