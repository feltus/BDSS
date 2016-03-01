# Installation

## Development

```
cd /path/to/bdss/client
python3 setup.py develop
```

## Stand alone executable

The client can also be built into a stand alone executable using [PyInstaller](http://www.pyinstaller.org/).
There are some caveats to this though. PyInstaller does not build a portable binary. See
http://pythonhosted.org/PyInstaller/#supporting-multiple-platforms for more information.

Requirements:

```Shell
apt-get install python3-dev
python3 setup.py install
pip install pyinstaller
```

Build:

```Shell
cd /path/to/bdss/client
pyinstaller --clean --onefile client.spec
```

## Transfer mechanisms

The BDSS client invokes other programs to transfer files. These must be installed individually.
