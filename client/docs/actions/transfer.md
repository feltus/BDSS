# Transfer Files

Transfer data files using a mechanism decided by the metadata repository.

The client will contact the metadata repository to request alternate data sources/transfer mechanisms for the
given URL(s) and will try each source/mechanism in order until the file is downloaded.

For each URL `transfer` is invoked with, it executes [this workflow](/client/docs/actions/transfer_workflow.svg).
