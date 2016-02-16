import argparse
import logging
import sys

from chalk import log

from .actions import all_actions, action_module


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

    for action in all_actions():
        action_parser = subparsers.add_parser(action)
        action_module(action).configure_parser(action_parser)

    args = parser.parse_args()
    logger.setLevel(getattr(logging, args.log.upper()))

    try:
        action_module(args.action).handle_action(args, parser)
    except:
        print("Failed", args.action, "action", file=sys.stderr)
        sys.exit(1)
