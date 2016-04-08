# Add Verification Method

This explains how to add support for a new verification method to the client.

Each verification method corresponds to a module in `client/verification` that conforms to
a specific API. To generate stub code for a new verification method, run
`./scripts/gen/verification id` from the BDSS project root, replacing `id` with the ID of
the new verification method. This will create a file at `client/verification/id.py` with
stubs for the required functions.

## Verification Method API

Each verification method module must have the following functions defined:

```Python
label = "Verification Method Name"
"""
A human readable name for the verification method. This will be displayed in the client's
log messages when attempting to verify transfers.
"""


def can_attempt_verification(transfer_spec, output_path):
    """
    Check if this method can try to verify the transfer. Returns True or False.

    Arguments:
    transfer_spec - TransferSpec - The specification of the transfer.
    output_path - str - The path to the downloaded file.
    """
    return True


def verify_transfer(transfer_spec, output_path):
    """
    Attempt to verify a transfer. Returns True if the transfer is verified,
    False if verification determined there was an error in the file, or raises
    an exception if verification was inconclusive.

    Arguments:
    transfer_spec - TransferSpec - The specification of the transfer.
    output_path - str - The path to the downloaded file.
    """
    raise NotImplementedError("%s verification is not implemented" % label)
```
