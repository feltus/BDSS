# Galaxy Tool

## Installation

* Copy `bdss.xml` into `/path/to/galaxy/tools/data_source`.
* [Build the BDSS client into a standalone executable](/client/docs/Installation.md).
* Set the path to the client executable in `bdss.xml`.
* [Configure the client](/client/docs/Configuration.md) to use the correct [metadata repository](/metadata_repository).
  The `.bdss.cfg` configuration file should be placed in the home directory of the user running the Galaxy server.
* [Make Galaxy aware of the new tool](https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial#A4._Make_Galaxy_aware_of_the_new_tool:).
* Restart Galaxy.

## Usage

The Galaxy tool takes two inputs: the manifest of URLs of data files and the maximum number of parallel processes
to use to download files.

* Select the "BDSS file transfer" tool under the "Get Data" section.
* Enter the list of data file URLs into the "Data URLs" text box and select the desired number of parallel processes.
* The tool will complete once all the files in the manifest are downloaded.
* Downloaded files may not automatically appear in the Galaxy history. You must manually refresh your history to
  see the files.

## References

* [Add tool tutorial](https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial)
* [Tool configuration syntax](https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax)
* [Number of Output datasets cannot be determined until tool run](https://wiki.galaxyproject.org/Admin/Tools/Multiple%20Output%20Files#Number_of_Output_datasets_cannot_be_determined_until_tool_run)
* [Example tool generating multiple datasets](https://web.science.mq.edu.au/~cassidy/2015/10/21/galaxy-tool-generating-datasets/)
