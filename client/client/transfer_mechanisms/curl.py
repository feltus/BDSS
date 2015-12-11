import subprocess
import sys


def transfer_data_file(url, output_path, options):
    subprocess.run(["curl", "--output", output_path, url], check=True, stderr=sys.stderr, stdout=sys.stdout)
