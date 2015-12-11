import argparse
import configparser
import os
import sys
import traceback
from collections import namedtuple
from pkg_resources import resource_string

import requests

from .transfer_mechanisms import default_mechanism, transfer_mechanism_module


TransferSpec = namedtuple("TransferSpec", "url transfer_mechanism transfer_mechanism_options")


def transfer_data_file(specs, output_path):
    print(specs)
    for s in specs:
        transfer_module = transfer_mechanism_module(s.transfer_mechanism)
        try:
            transfer_module.transfer_data_file(s.url, output_path, s.transfer_mechanism_options)
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

    config = configparser.ConfigParser()
    config.read_string(resource_string(__name__, "defaults.cfg").decode("utf-8"))
    config.read([os.path.expanduser("~/.bdss.cfg"), "bdss.cfg"])

    metadata_repository_url = config.get("metadata_repository", "url").rstrip("/")

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

        try:
            transfer_data_file(transfer_specs, output_path)
        except Exception:
            traceback.print_exc()
