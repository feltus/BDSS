# Big Data Smart Socket

## Getting started

### Set up [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/index.html):

```Shell
mkvirtualenv bdss
workon bdss
pip install -r requirements.txt
```

### Create database

Set `database_url` option in config/app.yml.
See [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls) for URL format.

```Shell
python create_db.py
```

### Configuration files

```Shell
cd BDSS/config
cp app.example.yml app.yml
cp data_transfer_methods.example.yml data_transfer_methods.yml
cp data_destinations.example.yml data_destinations.yml
```

### Apache VirtualHost configuration:

```ApacheConf
Listen 80
<VirtualHost *:80>
	DocumentRoot "/path/to/bdss/BDSS/static"

	<Directory "/path/to/bdss">
		Require all granted
	</Directory>

	WSGIDaemonProcess bdss user=user group=group processes=1 threads=5 \
		python-path=/path/to/virtualenvs/bdss/lib/python2.7/site-packages:/path/to/bdss/BDSS
	WSGIScriptAlias /api /path/to/bdss/bdss.wsgi

	<Location /api/>
		WSGIProcessGroup bdss
		WSGIApplicationGroup %{GLOBAL}
	</Location>

</VirtualHost>
```

### Start job processing daemon

```Shell
cd /path/to/bdss
python worker.py start
```
