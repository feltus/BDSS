import argparse
import logging
import sys

from chalk import log

from .actions import mechanisms_action, sources_action, test_files_action, transfer_action


logger = logging.getLogger("bdss")
handler = log.ChalkHandler()
handler.setFormatter(log.ChalkFormatter("%(asctime)s %(levelname)s - %(message)s"))
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="BDSS client")

    parser.add_argument("--log", choices=["debug", "info", "warn", "error"], default="info")

    subparsers = parser.add_subparsers(dest="action", metavar="action")

    mechanisms_parser = subparsers.add_parser("mechanisms", help="List available transfer mechanisms")
    mechanisms_action.configure_parser(mechanisms_parser)

    sources_parser = subparsers.add_parser("sources", help="Find data sources")
    sources_action.configure_parser(sources_parser)

    transfer_parser = subparsers.add_parser("transfer", help="Download data files")
    transfer_action.configure_parser(transfer_parser)

    test_files_parser = subparsers.add_parser("test-files", help="Get test file URLs")
    test_files_action.configure_parser(test_files_parser)

    args = parser.parse_args()
    logger.setLevel(getattr(logging, args.log.upper()))

    available_actions = {
        "mechanisms": mechanisms_action,
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
