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

import wtforms


label = "GridFTP-Lite"


description = "Transfer files with <a href=\"http://toolkit.globus.org/toolkit/data/gridftp/quickstart.html\">GridFTP-Lite</a> (GridFTP with SSH authentication)"


class OptionsForm(wtforms.Form):

    fast_mode = wtforms.fields.BooleanField(
        label="Transfer with -fast flag")

    parallelism = wtforms.fields.IntegerField(
        label="Parallelism",
        description="Number of parallel data connections to use (-parallel option)")

    block_size = wtforms.fields.IntegerField(
        label="Block Size",
        description="Buffer size (bytes) for underlying transfer method (-block-size option)")

    tcp_buffer_size = wtforms.fields.IntegerField(
        label="TCP Buffer Size",
        description="Buffer size (bytes) for underlying FTP data channels (-tcp-buffer-size option)")
