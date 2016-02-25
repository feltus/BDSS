For development:

(Preferably in a virtualenv)
```
cd /path/to/bdss/client
python3 setup.py develop
```

To build binary:

Requirements:

```Shell
apt-get install python3-dev
pip install pyinstaller
```

Build:

```Shell
cd /path/to/bdss/client
pyinstaller --onefile client.spec
```

Executable is output in `dist/bdss`
