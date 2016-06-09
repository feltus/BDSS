# Data Model

## Data Source

A data source contains both the location of files and the method for retrieving them from that
location. For example, files from [NCBI's SRA Archive](http://www.ncbi.nlm.nih.gov/sra) can be
downloaded from ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ using either FTP or
Aspera. Thus, the metadata repository would contain two data sources: one `NCBI SRA FTP` and
one `NCBI SRA Aspera`.

## URL Matcher

In order to identify if a file belongs to a data source known to the repository, each data source
has one or more URL matchers. These can be configured to match URLs with certain scheme(s)
and/or hostnames(s) or a more general regular expression.

## Transfer Mechanism

A source's transfer mechanism is the program that should be used to retrieve files from the
source. To use the NCBI example again, one data source would be set to use `ftp` as a
transfer mechanism, the other to use `ascp`. The data source can also have additional options
that are passed to the transfer mechanism. These are interpreted by the client and used to
build the command that will be used to invoke the mechanism. For example, the `ftp` mechanism
might provide a username option so that a data source could specify a username that is used
for anonymous access to its server.

## URL Transform

A URL transform defines how files from one data source are mapped to another data source. A
basic example would be an FTP mirror site where files are served from the exact same path
with the same method for retrieving them. In this case, the transform would simply replace
the hostname in the URL for file at the first data source with the hostname of the mirror
site to get a URL for the same file at the second data source.

A transform has a source and target data source and maps URLs from the source to the target.
Transforms should always link a slower source to a faster target.

## Test File

The URL matchers can determine data sources given a URL, but it can also be useful to go the
other way. The list of test files are known files at a specific data source. These can be
used for things like testing transfer speeds from the data source. Also, they provide some
validation of the data source's URL matcher configuration, as each test file URL is checked
against the data source's matchers when it is added.

## Timing Report

Each time the [BDSS client](/client/docs) is used to transfer a file, it sends a timing report
back to the metadata repository. This report contains:
* the file's URL
* the size of the file
* the time required to transfer the file
* a checksum

The file URL is used to link the report to a data source. This information can be used by
administrators to reconfigure the metadata repository to prioritize different data sources.
