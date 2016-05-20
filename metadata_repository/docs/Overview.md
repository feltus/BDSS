# Overview

The BDSS metadata repository maps URLs of data files to alternate sources for the same file.

* [Data Model](/metadata_repository/docs/DataModel.md)
* [Workflow for requesting alternate data sources](/metadata_repository/docs/core_workflow)

The metadata repository also collects analytics from the [BDSS client](/client/docs). Each time the client is
used to transfer a file, it reports back to the metadata repository the file's URL, the size of the file, the time
required to transfer the file, and a checksum. The file URL is used to link the
[report](/metadata_repository/docs/DataModel.md#timing-report) to a specific
[data source](/metadata_repository/docs/DataModel.md#data-source). This information can be used by administrators
to reconfigure the metadata repository to prioritize different data sources.
