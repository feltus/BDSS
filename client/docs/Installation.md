# Installation

The BDSS client requires Python 3.4+.

## Development

```Shell
git clone https://github.com/feltus/BDSS.git
cd BDSS/client
python3 setup.py develop
```

## Install from PyPI

_Not available yet_ (See [#105](https://github.com/feltus/BDSS/issues/105))

```Shell
pip install bdss-client
```

## Stand alone executable

The client can also be built into a stand alone executable using [PyInstaller](http://www.pyinstaller.org/).
There are some caveats to this though. PyInstaller does not build a portable binary. See
http://pythonhosted.org/PyInstaller/#supporting-multiple-platforms for more information.

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

## Transfer mechanisms

The BDSS client invokes other programs to transfer files. These must be installed individually. See the
[list of supported transfer mechanisms](/client/docs/transfer_mechanisms/README.md) for more information.
