# Installation

For setting up a local environment for development, see the
[developer documentation](/metadata_repository/docs/developer/DevelopmentEnvironment.md)

The metadata repository is a [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) application written
using the [Flask framework](http://flask.pocoo.org/docs/latest/). It also requires a relational database for storing
data. [SQLAlchemy](http://www.sqlalchemy.org/), the library used for database interactions, supports [several
different databases](http://docs.sqlalchemy.org/en/latest/dialects/index.html). The metadata repository is developed
and tested with [SQLite](https://www.sqlite.org) and [PostgreSQL](https://www.postgresql.org).

There are many [WSGI application servers](http://wsgi.readthedocs.io/en/latest/servers.html) available and Flask's
documentation explains some [options for deployment](http://flask.pocoo.org/docs/latest/deploying/). A few choices
are explained here.

## Apache + mod_wsgi

The instructions below are for an Ubuntu system. Commands may vary for other distributions.

1. Install Python 3.4+ and pip.
   ```Shell
   apt-get install python3-dev libffi-dev python3-pip
   ```

1. Install Apache and [mod_wsgi](https://modwsgi.readthedocs.io/en/latest/).
   ```Shell
   apt-get install apache2 apache2-dev
   pip3 install mod_wsgi
   mod_wsgi-express install-module
   echo "LoadModule wsgi_module $(mod_wsgi-express module-location)" > /etc/apache2/mods-available/wsgi_express.load
   echo "WSGIPythonHome /usr" > /etc/apache2/mods-available/wsgi_express.conf
   a2enmod wsgi_express
   service apache2 restart
   ```

1. Install metadata repository dependencies.
   ```Shell
   cd /path/to/metadata_repository
   pip3 install -r requirements.txt
   ```

1. Install a driver for your database of choice. See SQLAlchemy's
   [dialect documentation](http://docs.sqlalchemy.org/en/latest/dialects/index.html) for options.

1. Configure a [virtual host](https://httpd.apache.org/docs/current/vhosts/).
   Create a file at `/etc/apache2/sites-available/bdss_metadata_repository.conf` and add the following:
   ```ApacheConf
   <VirtualHost *:80>

       <Directory "/path/to/metadata_repository">
           Require all granted
       </Directory>

       Alias /static/ /path/to/metadata_repository/app/static/

       WSGIDaemonProcess bdss user=www-data group=www-data processes=1 threads=5 \
           python-path=/usr/local/lib/python3.5/dist-packages:/path/to/metadata_repository
       WSGIScriptAlias / /path/to/metadata_repository/app.wsgi
       WSGIProcessGroup bdss
       WSGIApplicationGroup %{GLOBAL}

   </VirtualHost>
   ```

   The `python-path` in `WSGIDaemonProcess` may vary based on your version of Python.

1. Configure the application.
   Create a `.env` file in the `metadata_repository` directory and add the following:
   ```
   DATABASE_URL=
   SESSION_KEY=
   ```

   The values for the options will depend on your specific configuration.

   * DATABASE_URL - Location of the database to use. See the
     [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) for more
     information. If you use a path to an SQLite database, it will be automatically created if it doesn't exist.
     For other database types, you may have to install an additional driver.

   * SESSION_KEY - Secret key for [Flask sessions](http://flask.pocoo.org/docs/latest/quickstart/#sessions). To
     generate a random key, run `dotenv set SESSION_KEY $(./scripts/generate_flask_key)`.

1. Run database migrations. The `with_dotenv` script loads environment variables from the `.env` file created
   in the last step.
   ```Shell
   cd /path/to/metadata_repository
   ./scripts/with_dotenv ./scripts/migrate
   ```

1. Disable default Apache site.
   ```Shell
   a2dissite 000-default
   ```

1. Enable BDSS site and restart Apache.
   ```Shell
   a2ensite bdss_metadata_repository
   service apache2 reload
   ```

For more information, see [mod_wsgi's documentation](https://modwsgi.readthedocs.io/en/latest/) or
[Flask's documentation on deploying with mod_wsgi](http://flask.pocoo.org/docs/latest/deploying/mod_wsgi/).

## Docker

The metadata repository can be also be deployed using [Docker](https://www.docker.com/products/docker).

The repository includes a [sample configuration file](/metadata_repository/deploy/docker/docker-compose-tiered.yml)
for [Docker Compose](https://docs.docker.com/compose/install/) to set up multiple app containers running
the metadata repository using [gunicorn](http://gunicorn.org/) behind an [nginx](https://www.nginx.com/) proxy
and backed by a [PostgreSQL](https://www.postgresql.org) database.
