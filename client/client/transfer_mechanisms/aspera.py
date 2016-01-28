import os
from urllib.parse import urlparse, urlunsplit

from .base import transfer_data_file_with_subprocess


def transfer_data_file(url, output_path, options):

    default_path_to_key = os.path.expandvars(os.path.join("$HOME", ".aspera", "connect", "etc", "asperaweb_id_dsa.openssh"))
    args = ["-i", default_path_to_key]

    # Require encryption?
    try:
        if options["disable_encryption"]:
            args.append("-T")
    except KeyError:
        pass

    # Remove scheme from URL
    parts = urlparse(url)
    url = parts[1] + urlunsplit(("", "", parts[2], parts[3], parts[4]))

    print(" ".join(["ascp"] + args + [options["username"] + "@" + url, output_path]))
    return transfer_data_file_with_subprocess(["ascp"] + args + [options["username"] + "@" + url, output_path])
