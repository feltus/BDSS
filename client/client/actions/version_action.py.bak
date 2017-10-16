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

import textwrap

from ..version import __version__


cli_help = "Print version and license information."


def configure_parser(parser):
    pass


def handle_action(args, parser):
    version_text = """
    bdss {version}
    Copyright (C) 2016 Clemson University
    License GPLv2: GNU GPL version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>.
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.
    """.format(version=__version__)
    print(textwrap.dedent(version_text).strip())
