from ..transfer_mechanisms import available_mechanisms


def configure_parser(parser):
    pass


def handle_action(args, parser):
    for m in available_mechanisms():
        print(m)
