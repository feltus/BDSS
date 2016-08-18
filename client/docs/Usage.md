# Usage

To see information about the BDSS client's command line interface, run `bdss help` or `bdss -h`.

This will show a list of available actions to take. Run `bdss <action> -h` to read about a specific action.

## Docker

To run bdss from the [Docker container](/client/docs/Installation.md#docker):

```Shell
docker run --rm --interactive --tty --volume="$PWD":/wd --workdir=/wd bdss-client help
```

Because the client runs inside the container, any file manifests or target directories passed as arguments to
transfer must be contained in the directory that is mounted as the container's working directory volume. Paths
should be relative to that directory.

## Actions

* mechanisms - [List available transfer mechanisms](/client/docs/actions/mechanisms.md)
* sources - [Find data sources](/client/docs/actions/sources.md)
* test_files - [Get test file URLs](/client/docs/actions/test_files.md)
* transfer - [Transfer files](/client/docs/actions/transfer.md)
