# Core Workflow

When a client requests alternate sources for a data file, it sends the file's URL. The metadata repository determines
which (if any) known [data sources](/metadata_repository/docs/DataModel.md#data-source) the URL may belong to using
the data sources' [URL matcher](/metadata_repository/docs/DataModel.md#url-matcher) configuration.

For each matching data source, each of the source's [URL transforms](/metadata_repository/docs/DataModel.md#url-transform)
are applied to the original data URL. The transform outputs an alternate URL for the data file and the transform's
target data source is configured with the [transfer mechanism](/metadata_repository/docs/DataModel.md#transfer-mechanism)
used to retrieve data from that source.

The metadata repository responds to the request with the list of alternate URLs and their corresponding transfer mechanism
information. The [BDSS client](/client/docs) interprets this information to launch the appropriate program to transfer
the file.

See the [workflow diagram](/metadata_repository/docs/core_workflow/workflow.svg) for a visual explanation.
