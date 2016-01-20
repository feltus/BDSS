import selectors
import subprocess
import sys


def transfer_data_file_with_subprocess(subprocess_args):
    process = subprocess.Popen(subprocess_args, bufsize=1,
                               stderr=subprocess.STDOUT, stdout=subprocess.PIPE, universal_newlines=True)

    output = ""
    def select_callback(stream, mask):
        nonlocal output
        line = stream.readline()
        output += line
        sys.stdout.write(line)

    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, select_callback)
    while process.poll() is None:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    return_code = process.wait()
    selector.close()

    success = (return_code == 0)

    return (success, output)
