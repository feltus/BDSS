# Add Transfer Mechanism Type

This explains how to add support for a type of new transfer mechanism to the metadata repository.

Each transfer mechanism type corresponds to modules in `app/transfer_mechanisms` in the metadata
repository and in `client/transfer/mechanisms` in the client that conform to a specific API. To
generate stub code for a new transfer mechanism type, run `./scripts/gen/transfer_mechanism id`
from the BDSS project root, replacing `id` with the ID of the new transfer mechanism type. This
will create files at `metadata_repository/app/transfer_mechanisms/id.py` and
`client/client/transfer/mechanisms/id.py` with stubs for the required functions.

See the [client documentation](/client/docs/developer/add_transfer_mechanism.md)
for information on the client's transfer mechanism module.

## Transfer Mechanism API

The metadata repository's transfer mechanism module must have the following functions defined:

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
