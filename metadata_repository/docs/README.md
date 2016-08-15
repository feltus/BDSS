# Overview

The BDSS metadata repository matches patterns of data file URLs and maps them to alternate sources for the same file.

* [Data Model](/metadata_repository/docs/DataModel.md)
* [Workflow for requesting alternate data sources](/metadata_repository/docs/core_workflow)

The metadata repository also collects analytics from the [BDSS client](/client/docs). Each time the client is
used to transfer a file, it reports back to the metadata repository the file's URL, the size of the file, the time
required to transfer the file, and a checksum. The file URL is used to link the
[report](/metadata_repository/docs/DataModel.md#transfer-report) to a specific
[data source](/metadata_repository/docs/DataModel.md#data-source). This information can be used by administrators
to reconfigure the metadata repository to prioritize different data sources.

## User documentation

* [Find alternate data URLs](/metadata_repository/docs/user/find_alternate_urls.md)
* [Search data sources](/metadata_repository/docs/user/search_data_sources.md)

## Administrator documentation

* [Add a data source](/metadata_repository/docs/admin/add_data_source.md)
* [Add a URL matcher](/metadata_repository/docs/admin/add_url_matcher.md)
* [Add a URL transform](/metadata_repository/docs/admin/add_url_transform.md)
* [Manage user permissions](/metadata_repository/docs/admin/manage_user_permissions.md)

## Developer documentation

* [Set up a development environment](/metadata_repository/docs/developer/DevelopmentEnvironment.md)
* [Code structure](/metadata_repository/docs/developer/CodeStructure.md)
* [Dependencies](/metadata_repository/docs/developer/Dependencies.md)
* How to add:
   * [URL matcher types](/metadata_repository/docs/developer/add_url_matcher_type.md)
   * [Transfer mechanisms](/metadata_repository/docs/developer/add_transfer_mechanism_type.md)
   * [URL transform types](/metadata_repository/docs/developer/add_url_transform_type.md)
