# Big Data Smart Socket

## Getting started

### Set up [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/index.html):

```Shell
mkvirtualenv bdss
workon bdss
pip install -r requirements.txt
```

### Configuration files

```Shell
cd BDSS/config
cp app.example.yml app.yml
cp data_transfer_methods.example.yml data_transfer_methods.yml
cp data_destinations.example.yml data_destinations.yml
```

### Create database

Set `database_url` option in BDSS/config/app.yml.
See [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls) for URL format.

```Shell
python create_db.py
```

### Generate secret key

Generate a random secret key for [Flask sessions](http://flask.pocoo.org/docs/0.10/quickstart/#sessions). This will be saved in BDSS/config/app.yml.

```Shell
python gen_key.py
```

### Apache VirtualHost configuration:

```ApacheConf
Listen 80
<VirtualHost *:80>

	<Directory "/path/to/bdss">
		Require all granted
	</Directory>

	Alias /static/ /path/to/bdss/BDSS/static/

	WSGIDaemonProcess bdss user=user group=group processes=1 threads=5 \
		python-path=/path/to/virtualenvs/bdss/lib/python2.7/site-packages:/path/to/bdss/BDSS
	WSGIScriptAlias /api /path/to/bdss/bdss.wsgi
	WSGIProcessGroup bdss
	WSGIApplicationGroup %{GLOBAL}

</VirtualHost>
```

### Start job processing daemon

```Shell
cd /path/to/bdss
python worker.py start
```
