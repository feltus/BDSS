###What is the Big Data Smart Socket (BDSS)?

The increasing size of datasets used in scientific computing has made it difficult or impossible for a researcher
to store all their data at the compute site they are using to process it. This has necessitated that a data transfer
step become a key consideration in experimental design. Accordingly, scientific data repositories such as NCBI have
begun to offer services such as dedicated data transfer machines and advanced transfer clients. Despite this,
many researchers continue familiar but suboptimal practices: using slow transfer clients like a web browser or `scp`,
transferring data over wireless networks, etc.

BDSS aims to alleviate this problem by shifting the burden of learning about alternative file mirrors, transfer
clients, tuning parameters, etc. from the end user researcher to a group of "data curators". It consists of three parts:

1. **[Metadata repository server](/metadata_repository/README.md)**
   * Central database managed by data curators
   * Maps URLs of data files to alternate sources
   * Includes information about the BDSS transfer client to use to access the data

2. **[BDSS transfer client](/client/README.md)**
   * Consumes information from metadata repository
   * Invokes transfer clients
   * Reports analytics to metadata repository

3. **[Integration as a Galaxy data transfer tool](/galaxy_tool/README.md)**
   * Run the BDSS client as part of a [Galaxy](https://galaxyproject.org/) workflow

