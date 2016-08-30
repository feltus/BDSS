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
   * [From the command line](https://github.com/feltus/BDSS/blob/master/client/docs)
   * [Command Line Usage Video](https://www.youtube.com/watch?v=Cwn7O5xssgY)
   * [From Galaxy](https://github.com/feltus/BDSS/blob/master/galaxy_tool/README.md)
   * [Galaxy Usage Video](https://www.youtube.com/watch?v=KE7KkA6rzMQ)
* [Managing an existing metadata repository](https://github.com/feltus/BDSS/blob/master/metadata_repository/docs/README.md#administrator-documentation)
* Setting up a new metadata repository
   * [For development or testing](https://github.com/feltus/BDSS/blob/master/metadata_repository/docs/developer/DevelopmentEnvironment.md)
   * [For production use](https://github.com/feltus/BDSS/blob/master/metadata_repository/docs/Installation.md)

## Examples

All examples here require a metadata repository configured to support them. The default metadata repository
at [http://bdss.bioinfo.wsu.edu/](http://bdss.bioinfo.wsu.edu/) supports these examples and the necessary
configuration is also listed here.

* [NCBI SRA archive](https://github.com/feltus/BDSS#ncbi-sra-archive)
* [JGI Genome Portal](https://github.com/feltus/BDSS#jgi-genome-portal)

### NCBI SRA archive

NCBI makes files available for [transfer using Aspera Connect](http://www.ncbi.nlm.nih.gov/books/NBK242625/),
a tool with "improved data transfer characteristics" vs FTP or HTTP. If `ascp` is installed on your machine,
BDSS can handle building the appropriate command.

Without BDSS:
```Shell
ascp -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh -T anonftp@ftp.ncbi.nlm.nih.gov:/sra/sra-instant/reads/ByRun/sra/SRR/SRR039/SRR039885/SRR039885.sra ./
```

With BDSS:
```Shell
bdss transfer -u 'ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR039/SRR039885/SRR039885.sra'
```

Metadata repository configuration:
```JSON
{
  "data_sources": [
    {
      "description": "",
      "label": "NCBI Sequence Read Archive with FTP",
      "test_files": [],
      "transfer_mechanism": {
        "options": {},
        "type": "curl"
      },
      "transforms": [
        {
          "for_destinations": [],
          "options": {
            "new_scheme": "aspera"
          },
          "target": "NCBI Sequence Read Archive with Aspera",
          "type": "change_scheme"
        }
      ],
      "url_matchers": [
        {
          "options": {
            "pattern": "^ftp://ftp\\.ncbi\\.nlm\\.nih\\.gov/sra"
          },
          "type": "regular_expression"
        }
      ]
    },
    {
      "description": "",
      "label": "NCBI Sequence Read Archive with Aspera",
      "test_files": [],
      "transfer_mechanism": {
        "options": {
          "disable_encryption": true,
          "username": "anonftp"
        },
        "type": "aspera"
      },
      "transforms": [],
      "url_matchers": [
        {
          "options": {
            "pattern": "^aspera://ftp\\.ncbi\\.nlm\\.nih\\.gov/sra"
          },
          "type": "regular_expression"
        }
      ]
    }
  ],
  "destinations": []
}
```

### JGI Genome Portal

To download files from the [JGI Genome Portal](http://genome.jgi.doe.gov/), you must first
[authenticate](http://genome.jgi.doe.gov/help/download.jsf#api). BDSS can prompt for credentials and
handle storing your session cookies.

Without BDSS:
```Shell
curl 'https://signon.jgi.doe.gov/signon/create' --data-urlencode 'login=USER_NAME' --data-urlencode 'password=USER_PASSWORD' -c cookies > /dev/null
curl 'http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism=PhytozomeV10' -b cookies > get-directory
```

With BDSS:
```Shell
bdss transfer -u 'http://genome.jgi.doe.gov/ext-api/downloads/get-directory?organism=PhytozomeV10'
JGI Genome Portal username?USER_NAME
JGI Genome Portal password?USER_PASSWORD
```

Metadata repository configuration:
```JSON
{
  "data_sources": [
    {
      "description": "",
      "label": "JGI Genome Portal",
      "test_files": [],
      "transfer_mechanism": {
        "options": {
          "auth_url": "https://signon.jgi.doe.gov/signon/create",
          "password_field": "password",
          "password_prompt": "JGI Genome Portal password?",
          "username_field": "login",
          "username_prompt": "JGI Genome Portal username?"
        },
        "type": "session_authenticated_curl"
      },
      "transforms": [],
      "url_matchers": [
        {
          "options": {
            "pattern": "http:\\/\\/genome\\.jgi\\.doe\\.gov\\/ext-api"
          },
          "type": "regular_expression"
        }
      ]
    }
  ],
  "destinations": []
}
```
