from .base import transfer_data_file_with_subprocess


def transfer_data_file(url, output_path, options):
    return transfer_data_file_with_subprocess(["curl", "--output", output_path, url])
