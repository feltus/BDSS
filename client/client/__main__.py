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

import argparse
import logging
import pkg_resources
import sys
import textwrap
import traceback

from chalk import log

from .actions import action_module, available_action_info


logger = logging.getLogger("bdss")
handler = log.ChalkHandler()
handler.setFormatter(log.ChalkFormatter("%(asctime)s %(levelname)s - %(message)s"))
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="BDSS client")

    parser.add_argument("--log", choices=["debug", "info", "warn", "error"], default="info",
                        help="Level of log messages to print. One of debug, info, warn, error.", metavar="level")
    parser.add_argument("--version", "-v", action="store_true")

    subparsers = parser.add_subparsers(dest="action",
                                       help="description",
                                       metavar="action",
                                       title="available actions")

    for action, help_text in available_action_info():
        action_parser = subparsers.add_parser(action, help=help_text)
        action_module(action).configure_parser(action_parser)

    args = parser.parse_args()

    if args.version:
        version_text = """
        bdss {version}
        Copyright (C) 2016 Clemson University
        License GPLv2: GNU GPL version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>.
        This is free software: you are free to change and redistribute it.
        There is NO WARRANTY, to the extent permitted by law.
        """.format(version=pkg_resources.require("bdss_client")[0].version)
        print(textwrap.dedent(version_text).strip())
        sys.exit(1)

    logger.setLevel(getattr(logging, args.log.upper()))

    if not args.action:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    try:
        action_module(args.action).handle_action(args, parser)
    except Exception as e:
        logger.error("Failed %s action" % args.action)
        logger.error(e)
        logger.debug(traceback.format_exc())
        sys.exit(1)
