import argparse
import os
import sys
import time
import traceback
from collections import namedtuple

import requests

from .config import metadata_repository_url
from .transfer_mechanisms import default_mechanism, transfer_mechanism_module

TransferSpec = namedtuple("TransferSpec", "url transfer_mechanism transfer_mechanism_options")


def send_timing_report(data_file_url, file_size_bytes, transfer_duration_seconds):
    """
    Send a timing report to the metadata repository.

    Parameters:
    data_file_url - String - The URL of the data file that was transferred.
    file_size_bytes - Integer - The size of the data file (in bytes).
    transfer_duration_seconds - Float - The time required to download the file (in seconds).
    """
    requests.post(metadata_repository_url + "/timing_reports",
                  data={
                      "url": data_file_url,
                      "file_size_bytes": file_size_bytes,
                      "transfer_duration_seconds": transfer_duration_seconds
                  })


def transfer_data_file(specs, output_path):
    """
    Transfer a data file.

    Parameters:
    specs - TransferSpec[] - List of TransferSpecs for difference sources for the data file.
    output_path - String - The path to save the downloaded file to.
    """
    print(specs)
    for s in specs:
        transfer_module = transfer_mechanism_module(s.transfer_mechanism)
        start_time = time.time()
        try:
            transfer_module.transfer_data_file(s.url, output_path, s.transfer_mechanism_options)
            time_elapsed = time.time() - start_time
            file_size = os.stat(output_path).st_size
            send_timing_report(s.url, file_size, time_elapsed)
            return True
        except Exception:
            traceback.print_exc()

    return False


def main():
    parser = argparse.ArgumentParser(description="BDSS client")

    parser.add_argument("urls",
                        help="URLs of data files to download",
                        metavar="data-file-urls",
                        nargs="*")

    parser.add_argument("-m", "--url-manifest",
                        dest="manifest_file",
                        help="Path to file containing a list of URLs of data files to download.",
                        type=argparse.FileType("r"))

    args = parser.parse_args()

    if args.manifest_file:
        args.urls = [line.strip() for line in args.manifest_file if line.strip()]

    if not args.urls:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    for url in args.urls:

        output_path = url.partition("?")[0].rpartition("/")[2]
        transfer_specs = None

        try:
            response = requests.post("%s/transformed_urls" % metadata_repository_url,
                                     data={"url": url},
                                     headers={"Accept": "application/json"})

            print(response.text)
            response = response.json()

            transfer_specs = [TransferSpec(r["transformed_url"],
                              r["transform_applied"]["to_data_source"]["transfer_mechanism_type"],
                              r["transform_applied"]["to_data_source"]["transfer_mechanism_options"]) for r in response["results"]]

        except Exception:
            traceback.print_exc()

        if not transfer_specs:
            transfer_specs = [TransferSpec(url, *default_mechanism(url))]

        if not transfer_data_file(transfer_specs, output_path):
            print("Failed to download file", file=sys.stderr)
