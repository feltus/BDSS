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


def transfer_data_file(specs):
    print(specs)
    for s in specs:
        transfer_module = transfer_mechanism_module(s.transfer_mechanism)
        try:
            print("Downloading %s..." % s.url)
            print(transfer_module)
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
        try:
            response = requests.post("%s/transformed_urls" % metadata_repository_url,
                                     data={"url": url},
                                     headers={"Accept": "application/json"})

            print(response.text)
            response = response.json()

            specs = [TransferSpec(r["transformed_url"],
                                  r["transform_applied"]["to_data_source"]["transfer_mechanism_type"],
                                  r["transform_applied"]["to_data_source"]["transfer_mechanism_options"]) for r in response["results"]]

            if specs:
                transfer_data_file(specs)
            else:
                transfer_data_file([TransferSpec(url, *default_mechanism(url))])
        except Exception:
            traceback.print_exc()
            transfer_data_file([TransferSpec(url, *default_mechanism(url))])
