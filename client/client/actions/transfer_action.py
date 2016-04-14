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
import hashlib
import json
import logging
import os
import sys
import time
import traceback

import requests

from ..config import metadata_repository_url
from ..transfer import TransferSpec
from ..transfer.mechanisms import available_mechanisms, default_mechanism
from ..transfer.script import generate_script
from ..verification import verify_transfer


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

    input_group.add_argument("--input-spec", "-i",
                             dest="spec_input_file",
                             help="File containing transfer specs to run",
                             type=argparse.FileType("r"))

    parser.add_argument("--destination", "-d",
                        dest="destination_directory",
                        default=os.getcwd(),
                        help="Path to directory to store downloaded files in")

    output_group = parser.add_mutually_exclusive_group(required=False)

    output_group.add_argument("--output-script",
                              action="store_true",
                              help="Instead of transferring files, output script that can be used to transfer them")

    output_group.add_argument("--output-spec", "-o",
                              dest="spec_output_file",
                              help="Path to output succesful transfer specs",
                              type=argparse.FileType("w"))


def file_md5sum(filename):
    """
    Calculate the MD5 hash of a file.

    Parameters:
    filename - String - The name of the file.
    """
    h = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def send_timing_report(success, data_file_url, file_size_bytes, transfer_duration_seconds, file_checksum, mechanism_output):
    """
    Send a timing report to the metadata repository.

    Parameters:
    data_file_url - String - The URL of the data file that was transferred.
    file_size_bytes - Integer - The size of the data file (in bytes).
    transfer_duration_seconds - Float - The time required to download the file (in seconds).
    file_checksum - String - The MD5 checksum of the downloaded file.
    mechanism_output - String - The output of the transfer mechanism used.
    """
    requests.post(metadata_repository_url + "/timing_reports",
                  data={
                      "is_success": success,
                      "url": data_file_url,
                      "file_size_bytes": file_size_bytes,
                      "transfer_duration_seconds": transfer_duration_seconds,
                      "file_checksum": file_checksum,
                      "mechanism_output": mechanism_output
                  })


def transfer_data_file(specs, output_path, spec_output_file=None):
    """
    Transfer a data file.

    Parameters:
    specs - TransferSpec[] - List of TransferSpecs for difference sources for the data file.
    output_path - String - The path to save the downloaded file to.
    """
    for s in specs:
        logger.debug("Downloading %s using %s", s.url, s.transfer_mechanism)
        if s.transfer_mechanism_options:
            logger.debug("%s options:", s.transfer_mechanism)
            for k, v in s.transfer_mechanism_options.items():
                logger.debug("  %s: %s", k, str(v))

        start_time = time.time()

        # This assumes transfer_data_file returns an object with a "stdout" member containing the output of
        # the transfer mechanism. Or if it throws an exception, the exception has a "stdout" member.
        # This is true if transfer_data_file returns the result of subprocess.run.
        success = False
        mechanism_output = ""
        try:
            logger.info(" ".join(s.transfer_command(output_path)))
            (success, mechanism_output) = s.run_transfer(output_path)
        except Exception:
            logger.exception("Exception in transfer mechanism")
        finally:
            time_elapsed = time.time() - start_time
            file_size = 0
            file_checksum = None
            if os.path.isfile(output_path):
                file_size = os.stat(output_path).st_size
                file_checksum = file_md5sum(output_path)
            try:
                send_timing_report(success, s.url, file_size, time_elapsed, file_checksum, mechanism_output)
            except:
                logger.warn("Failed to send timing report")
                logger.debug(traceback.format_exc())
            if success:
                logger.info("Success. Downloaded %d bytes in %d seconds", file_size, time_elapsed)
                if spec_output_file:
                    spec_output_file.write(json.dumps({
                        "url": s.url,
                        "transfer_mechanism": s.transfer_mechanism,
                        "transfer_mechanism_options": s.transfer_mechanism_options
                    }))
                return verify_transfer(s, output_path)
            else:
                logger.warn("Unable to download file")
                if file_size != 0:
                    logger.warn("Failed after %d seconds. %d bytes downloaded", time_elapsed, file_size)

    return False


def output_file_name(url):
    return url.partition("?")[0].rpartition("/")[2]


def request_transfer_specs(url):
    transfer_specs = []

    data = {"available_mechanisms-" + str(i): mech for i, mech in enumerate(available_mechanisms())}
    data["url"] = url

    response = requests.post("%s/transformed_urls" % metadata_repository_url,
                             data=data,
                             headers={"Accept": "application/json"})

    response = response.json()

    transfer_specs = [TransferSpec(r["transformed_url"],
                      r["transform_applied"]["to_data_source"]["transfer_mechanism_type"],
                      r["transform_applied"]["to_data_source"]["transfer_mechanism_options"]) for r in response["results"]]

    if transfer_specs:
        logger.info("Received alternate data sources")
        logger.info("-------")
        for r in response["results"]:
            logger.info("%s", r["transform_applied"]["to_data_source"]["label"])
            logger.info("  %s", r["transformed_url"])
            logger.info("  %s", r["transform_applied"]["to_data_source"]["transfer_mechanism_type"])
    else:
        logger.warn("Received no alternate data sources")

    return transfer_specs


def handle_action(args, parser):
    if args.manifest_file:
        args.urls = [line.strip() for line in args.manifest_file if line.strip()]

    if not args.urls and not args.spec_input_file:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    urls_to_transfer = []

    if args.urls:
        for url in args.urls:
            transfer_specs = []
            try:
                logger.info("Requesting alternate sources for %s" % url)
                transfer_specs = request_transfer_specs(url)
            except Exception:
                logger.warn("Failed to load transfer specs from metadata repository")
                logger.debug(traceback.format_exc())

            transfer_specs.append(TransferSpec(url, *default_mechanism(url)))

            urls_to_transfer.append({
                "url": url,
                "output_file_name": output_file_name(url),
                "transfer_specs": transfer_specs
            })

    elif args.spec_input_file:
        for line in args.spec_input_file:
            if not line.rstrip():
                continue
            s = json.loads(line)
            transfer_spec = TransferSpec(s["url"], s["transfer_mechanism"], s["transfer_mechanism_options"])
            urls_to_transfer.append({
                "url": s["url"],
                "output_file_name": output_file_name(s["url"]),
                "transfer_specs": [transfer_spec]
            })

    if args.output_script:
        print(generate_script(urls_to_transfer))

    else:
        os.makedirs(args.destination_directory, exist_ok=True)
        for u in urls_to_transfer:
            output_path = os.path.join(args.destination_directory, u["output_file_name"])
            if os.path.isfile(output_path):
                logger.warn("File at %s already exists at %s", u["url"], output_path)
                continue

            if not transfer_data_file(u["transfer_specs"], output_path, args.spec_output_file):
                logger.error("Failed to download file")
