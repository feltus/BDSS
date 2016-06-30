# Add Transfer Mechanism Type

This explains how to add support for a type of new transfer mechanism to the client.

Each transfer mechanism type corresponds to a module in `app/transfer_mechanisms` in the metadata
repository and a class in `client/transfer/mechanisms` in the client that conform to a specific API.
To generate stub code for a new transfer mechanism type, run `./scripts/gen/transfer_mechanism id`
from the BDSS project root, replacing `id` with the ID of the new transfer mechanism type. This
will create files at `metadata_repository/app/transfer_mechanisms/id.py` and
`client/client/transfer/mechanisms/id.py` with stubs for the required functions.

See the [metadata repository documentation](/metadata_repository/docs/developer/add_transfer_mechanism.md)
for information on the metadata repository's transfer mechanism module.

## Transfer Mechanism API

The client transfer mechanism class must implement the following interface as defined in
`client.transfer.mechanisms.base.BaseMechanism`:

```Python
class Mechanism():

    @classmethod
    def allowed_options(self):
        """
        List of option names to filter options passed from metadata repository against.

        Returns:
        String[] - Names of options to allow.
        """
        return []

    @classmethod
    def is_available(cls):
        """
        Determine if the transfer mechanism is available on this machine.
        Usually involves checking if a specific program is found on the PATH.

        Returns:
        Boolean - True if available
        """
        raise NotImplementedError

    def transfer_file(self, url, output_path):
        """
        Transfer a file.

        Parameters:
        url - String - URL of the file to transfer
        output_path - String - Path to write transferred file to

        Returns:
        (Boolean, String) - Tuple of (True/False for success/failure, Mechanism output)
        """
        raise NotImplementedError

    def user_input_options(self):
        """
        Define options whose values must be supplied by the end user.

        Returns:
        UserInputOption[]
        """
        return []
```
