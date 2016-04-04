# Add Transfer Mechanism Type

This explains how to add support for a type of new transfer mechanism to the metadata repository.

Each transfer mechanism type corresponds to modules in `app/transfer_mechanisms` in the metadata
repository and in `client/transfer/mechanisms` in the client that conform to a specific API. To
generate stub code for a new transfer mechanism type, run `./scripts/gen/transfer_mechanism id`
from the BDSS project root, replacing `id` with the ID of the new transfer mechanism type. This
will create files at `metadata_repository/app/transfer_mechanisms/id.py` and
`client/client/transfer/mechanisms/id.py` with stubs for the required functions.

## Transfer Mechanism API

The transfer mechanism modules must have the following functions defined:

### Metadata Repository Module

```Python
label = "Mechanism Name"
"""
A human readable name for the transfer mechanism. This will be displayed in the list of
available mechanisms when adding or editing a data source.
"""


description = "Transfer files with some program"
"""
Human readable description of how the mechanism operates. This will be displayed
when the user selects this mechanism when adding or editing a data source.
"""


class OptionsForm(wtforms.Form):
    """
    Mechanism options form displayed when adding/editing a data source.
    Must be a subclass of wtforms.Form.
    """
    pass

```

### Client Module

```Python
def is_available():
    """
    Check if the mechanism is available on the client's machine. Returns True or False.
    Usually involves checking if a specific program is found on the PATH.
    """
    return True


def transfer_command(url, output_path, options):
    """
    Return the command used to transfer a file with this mechanism and the given options.
    Returns a list (to be passed to subprocess.Popen).

    Arguments:
    url - str - URL of the file to transfer.
    output_path - str - Path to save the file data to.
    options - dict - Mechanism options from the OptionsForm at the metatdata repository.
                     Keys match field names in the form and values are form input values.
    """
    return ["curl", "-o", output_path, url]
```
