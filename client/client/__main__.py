import argparse
import sys

from .actions import test_files_action, transfer_action


def main():
    parser = argparse.ArgumentParser(description="BDSS client")

    subparsers = parser.add_subparsers(dest="action", metavar="action")

    transfer_parser = subparsers.add_parser("transfer", help="Download data files")
    transfer_action.configure_parser(transfer_parser)

    test_files_parser = subparsers.add_parser("test-files", help="Get test file URLs")
    test_files_action.configure_parser(test_files_parser)

    args = parser.parse_args()

    if args.action == "transfer":
        transfer_action.transfer_files(args, parser)
    elif args.action == "test-files":
        test_files_action.print_test_files(args, parser)
    else:
        parser.print_help(file=sys.stderr)
        sys.exit(1)
