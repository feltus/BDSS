# Find Alternate URLs

Finding alternate URLs for data files is the core functionality of the BDSS metadata repository.
Usually, this will handled by the [BDSS client](/client/docs/README.md) during a file
[transfer](/client/docs/actions/transfer.md). However, a user can also view the same information
that the client would fetch directly on the metadata repository's website.

1. Log in to the metadata repository.

2. On the home screen, click "Find Alternate Data Sources".

3. The form has two inputs: "Available Mechanisms" and "URL".

   * The URL input is the URL of the data file you want to find alternate sources for.

   * The Available Mechanisms allows you to filter results to only data sources using specific
     transfer mechanisms. Each entry in the Available Mechanisms list should be the ID of a
     transfer mechanism.

4. Submit the form.

5. Each entry in the output will show the original URL and the transformed URL as well as the
   name of the original data source, the ID of the transform applied, and the name of the
   target data source.
