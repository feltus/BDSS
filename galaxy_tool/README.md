# Galaxy Tool

## Installation

* Copy `bdss.xml` into `/path/to/galaxy/tools/data_source`.
* [Build the BDSS client into a standalone executable](/client/docs/Installation.md).
* Set the path to the client executable in `bdss.xml`.
* [Configure the client](/client/docs/Configuration.md) to use the correct metadata repository.
  The `.bdss.cfg` configuration file should be placed in the directory of the user running the Galaxy server.
* [Make Galaxy aware of the new tool](https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial#A4._Make_Galaxy_aware_of_the_new_tool:).
* Restart Galaxy.


## Usage

The Galaxy tool takes one input: the data manifest as a text dataset.

* Your data manifest should be a plain text file with one data file URL per line.
* Select the `Get Data -> Upload File` tool.
* Click `Choose Local File`, select a file, and upload your data manifest.
* Select the `Get Data -> BDSS` tool.
* Choose the file uploaded by the `Upload File` tool for the `Data Manifest` option and execute.
* The tool will complete once all the files in the manifest are downloaded.

## References

* [Add tool tutorial](https://wiki.galaxyproject.org/Admin/Tools/AddToolTutorial)
* [Tool configuration syntax](https://wiki.galaxyproject.org/Admin/Tools/ToolConfigSyntax)
* [Number of Output datasets cannot be determined until tool run](https://wiki.galaxyproject.org/Admin/Tools/Multiple%20Output%20Files#Number_of_Output_datasets_cannot_be_determined_until_tool_run)
* [Example tool generating multiple datasets](https://web.science.mq.edu.au/~cassidy/2015/10/21/galaxy-tool-generating-datasets/)
