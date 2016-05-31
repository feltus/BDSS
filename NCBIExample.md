# NCBI Example

While developing this tool, one of the primary uses cases considered was the [National Center for Biotechnology
Information](http://www.ncbi.nlm.nih.gov/)'s [Sequence Read Archive](http://www.ncbi.nlm.nih.gov/sra). In this
case, there is an [FTP server](ftp://ftp-trace.ncbi.nlm.nih.gov/sra/) hosting biological sequence data. NCBI
also supports using [Aspera Connect for data transfers](http://www.ncbi.nlm.nih.gov/books/NBK242625/). The goal
here would be transfer the file using the faster Aspera client even if the user requests a file from a URL pointing
to the FTP server.

In this case, the [metadata repository](/metadata_repository/docs/README.md) would be configured with two [data
sources](/metadata_repository/docs/DataModel.md#data-source):

* NCBI SRA FTP
* NCBI SRA Aspera

The NCBI SRA FTP data source would be configured with a [URL Matcher](/metadata_repository/docs/DataModel.md#url-matcher)
that matches URLs with scheme FTP and host ftp-trace.ncbi.nlm.nih.gov. It would also be configured with a [URL
transform](/metadata_repository/docs/DataModel.md#url-transform) that mapped URLs from the FTP data source to the
Aspera data source by replacing the URL scheme.

The Aspera data source would be configured to use Aspera as the [transfer
mechanism](/metadata_repository/docs/DataModel.md#transfer-mechanism) and would also store the [Aspera client
parameters required for NCBI](http://www.ncbi.nlm.nih.gov/books/NBK242625/#Aspera_Transfer_Guide_BK.Using_ascp_to_D).

When a user attempts to transfer a file from the SRA FTP server, such as
ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR039/SRR039884/SRR039884.sra, using the BDSS
transfer client, the following happens:

1. Client requests alternate URLs for the file from the metadata repository.
1. Metadata repository uses URL matcher configuration to match URL to NCBI SRA FTP data source.
1. Metadata repository applies NCBI SRA FTP data source's URL transforms to URL to map URL to Aspera data source.
1. Metadata repository responds with alternate URL and transfer mechanism (Aspera) information.
1. Client uses Aspera to download file.
