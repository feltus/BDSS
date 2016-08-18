# What is the Big Data Smart Socket (BDSS)?

The increasing size of datasets used in scientific computing has made it difficult or impossible for a researcher
to store all their data at the compute site they are using to process it. This has necessitated that a data transfer
step become a key consideration in experimental design. Accordingly, scientific data repositories such as NCBI have
begun to offer services such as dedicated data transfer machines and advanced transfer clients. Despite this,
many researchers continue familiar but suboptimal practices: using slow transfer clients like a web browser or `scp`,
transferring data over wireless networks, etc.

BDSS aims to alleviate this problem by shifting the burden of learning about alternative file mirrors, transfer
clients, tuning parameters, etc. from the end user researcher to a group of "data curators". It consists of three parts:

## Components

* Metadata repository
   * Central database managed by data curators
   * Matches patterns of data file URLs and maps them to alternate sources
   * Includes information about the transfer tool to use to retrieve the data

* BDSS transfer client
   * Consumes information from metadata repository
   * Invokes transfer tools
   * Reports analytics to metadata repository

* Integration as a [Galaxy](https://galaxyproject.org/) data transfer tool

## Get Started

* Moving data with the BDSS client:
   * [From the command line](/client/docs)
   * [From Galaxy](/galaxy_tool/README.md)
* [Managing an existing metadata repository](/metadata_repository/docs/README.md#administrator-documentation)
* Setting up a new metadata repository
   * [For development or testing](/metadata_repository/docs/developer/DevelopmentEnvironment.md)
   * [For production use](/metadata_repository/docs/Installation.md)
