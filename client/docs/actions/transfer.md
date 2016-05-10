# Transfer Files

Transfer data files using a mechanism decided by the metadata repository.

The client will contact the metadata repository to request alternate data sources/transfer mechanisms for the
given URL(s) and will try each source/mechanism in order until the file is downloaded.

For each URL `transfer` is invoked with, it executes [this workflow](/client/docs/actions/transfer_workflow.svg).

It will often be useful to execute multiple transfers in parallel. [xargs](http://ss64.com/bash/xargs.html) is
useful for this. `xargs -n 1 -P numprocs bdss transfer --urls < manifest.txt` will execute `numprocs` parallel
transfers.
