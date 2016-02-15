from .base import is_program_on_path, transfer_data_file_with_subprocess


def is_available():
    return is_program_on_path("curl")


def transfer_data_file(url, output_path, options):
    return transfer_data_file_with_subprocess(["curl", "--output", output_path, url])
