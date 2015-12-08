import argparse
import configparser
import os
import sys
from pkg_resources import resource_string


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

    print(config.get("metadata_repository", "url"))
