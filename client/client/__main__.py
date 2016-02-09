import argparse
import sys

from .actions import sources_action, test_files_action, transfer_action


def main():
    parser = argparse.ArgumentParser(description="BDSS client")

    subparsers = parser.add_subparsers(dest="action", metavar="action")

    sources_parser = subparsers.add_parser("sources", help="Find data sources")
    sources_action.configure_parser(sources_parser)

    transfer_parser = subparsers.add_parser("transfer", help="Download data files")
    transfer_action.configure_parser(transfer_parser)

    test_files_parser = subparsers.add_parser("test-files", help="Get test file URLs")
    test_files_action.configure_parser(test_files_parser)

    args = parser.parse_args()

    available_actions = {
        "sources": sources_action,
        "transfer": transfer_action,
        "test-files": test_files_action
    }

    if args.action in available_actions:
        try:
            available_actions[args.action].handle_action(args, parser)
        except:
            print("Failed", args.action, "action", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help(file=sys.stderr)
        sys.exit(1)
