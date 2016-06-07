# Installation

The BDSS client requires Python 3.4+.

## Development

```Shell
git clone https://github.com/feltus/BDSS.git
cd BDSS/client
python3 setup.py develop
```

See Python's [documentation on installing modules](https://docs.python.org/3/install/) for more information.

## Install from PyPI

_Not available yet_ (See [#105](https://github.com/feltus/BDSS/issues/105))

```Shell
pip install bdss-client
```

## Stand alone executable

### Using system Python

The client can also be built into a stand alone executable using [PyInstaller](http://www.pyinstaller.org/).
There are some caveats to this though. PyInstaller does not build a portable binary. See
http://pythonhosted.org/PyInstaller/#supporting-multiple-platforms for more information.
This also requires that your current version of Python be 3.4+ and you are able to install
all dependencies in `requirements.txt`.

Requirements:

```Shell
apt-get install python3-dev
pip install pyinstaller
```

Build:

```Shell
cd /path/to/BDSS/client
pyinstaller --clean --onefile client.spec
```

### Self contained install

Alternatively, you can download and compile a version of Python specifically for the
installation. This removes all dependency on the system Python and libraries. There
is a script available to do this automatically.

```Shell
cd /path/to/BDSS/client
./scripts/bundle
```

Compiling Python does require some OS packages to be installed.

On Debian/Ubuntu:
```Shell
apt-get install openssl libssl-dev
```

## Transfer mechanisms

The BDSS client invokes other programs to transfer files. These must be installed individually. See the
[list of supported transfer mechanisms](/client/docs/transfer_mechanisms/README.md) for more information.

## Docker

To build a Docker container with the BDSS client:

```Shell
cd /path/to/bdss/client
docker build -t bdss-client .
```
