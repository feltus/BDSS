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
import os
import traceback
import tempfile

import requests

from ..config import client_destination, metadata_repository_url, dtn_host, dtn_user, dtn_path
from ..transfer.base import Transfer
from ..transfer.data import run_data_transfer
from ..transfer.mechanisms import available_mechanisms
from ..transfer.reporting import ReportsFile, send_report
from ..util import run_subprocess


cli_help = "Download data file(s)."


logger = logging.getLogger("bdss")


def configure_parser(parser):

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument("manifest_file",
                             help="File containing a list of URLs to transfer",
                             nargs="?",
                             type=argparse.FileType("r"))

    input_group.add_argument("--urls", "-u",
                             dest="urls",
                             help="URL(s) of data files to transfer",
                             metavar="URL",
                             nargs="+")

    parser.add_argument("--destination", "-d",
                        dest="destination_directory",
                        default=os.getcwd(),
                        help="Path to directory to store transferred files in")

    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Display available sources for files, but do not transfer")

    parser.add_argument("--transfer-report", "-t",
                        dest="report_file",
                        help="Path to write transfer report to",
                        type=argparse.FileType("w"))


def output_file_name(url):
    return url.partition("?")[0].rpartition("/")[2]


def get_transfers(url, mechanisms):
    transfers = []

    data = dict(
        available_mechanisms=mechanisms,
        url=url
    )
    if client_destination:
        data["destination"] = client_destination

    logger.info("Requesting transfers for %s" % url)
    try:
        response = requests.post("%s/transfers" % metadata_repository_url,
                                 data=data,
                                 headers={"Accept": "application/json"})

        response = response.json()

        transfers = [Transfer(**r) for r in response["transfers"]]

        if not transfers:
            logger.warn("Received no transfers")

    except:
        logger.warn("Request for transfers failed")
        logger.debug(traceback.format_exc())

    # As a last resort, fall back to original URL and its default mechanism
    # Defaults are defined in mechanisms/__init__ module
    default_transfer = Transfer(url)
    if default_transfer not in transfers:
        transfers.append(default_transfer)

    return transfers

def handle_dtn_action(args, parser, reports_file):
    # We want to download into a temporary file.
    tf = tempfile.NamedTemporaryFile()
    dest_dir = "".join([dtn_path, '/', tf.name])

    conn_str = "%s@%s" %  (dtn_user, dtn_host)
    logger.info("Initiating transfer with DTN: %s", conn_str)

    # Download the files using the DTN by calling BDSS on that server instead.
    bdss_cmd = " ".join(['bdss', 'transfer', '--urls', " ".join(args.urls), '--destination', dest_dir])
    run_subprocess(["ssh", conn_str, bdss_cmd])

    # Move the files to where they should be.
    logger.info("Copying files from DTN...")
    run_subprocess(["scp", "-r", "%s:%s/*" % (conn_str, dest_dir), args.destination_directory])

    # Finally delete the files on the remote server
    logger.info("Removing from from DTN...")
    run_subprocess(["ssh", conn_str, "rm -rf %s" % dest_dir])

def handle_local_action(args, parser, reports_file):
    for url in args.urls:
        output_path = os.path.abspath(os.path.join(args.destination_directory, output_file_name(url)))
        if os.path.isfile(output_path):
            logger.warn("File at %s already exists at %s", url, output_path)
            continue

        transfers = get_transfers(url, available_mechanisms())

        logger.info("%d transfer(s) for %s", len(transfers), url)
        logger.info("------------------")
        for t in transfers:
            logger.info(str(t))

        if args.dry_run:
            continue

        transfer_success = False
        for t in transfers:
            report = run_data_transfer(t, output_path)

            if report.success:
                transfer_success = True
                logger.info("Transfer successful")
                logger.debug(report)
                send_report(report)
                if reports_file:
                    reports_file.write_report(report)
                break
            else:
                logger.warn("Transfer failed")
                send_report(report)

        if not transfer_success:
            logger.error("Failed to transfer file")

def handle_action(args, parser):
    if args.manifest_file:
        args.urls = [line.strip() for line in args.manifest_file if line.strip()]

    os.makedirs(args.destination_directory, exist_ok=True)
    reports_file = ReportsFile(args.report_file) if args.report_file else None

    if dtn_host:
        handle_dtn_action(args, parser, reports_file)
    else:
        handle_local_action(args, parser, reports_file)
