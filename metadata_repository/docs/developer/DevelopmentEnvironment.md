# Development Environment

## Docker

Install Docker and Docker Compose.

1. Start services
   ```
   cd /path/to/metadata_repository
   docker-compose -f docker-compose.yml -f development.yml up
   ```

   The default configuration is to copy application files to the container and runs the metadata repository application
   using [gunicorn](http://gunicorn.org/). Adding the `development.yml` file overrides this and mounts the current
   directory and runs the [Flask development server in debug mode](http://flask.pocoo.org/docs/0.10/quickstart/#debug-mode).
   This allows for files to be edited on the host and the container to detect changes and restart the app server.

2. Generate a secret key for [Flask sessions](http://flask.pocoo.org/docs/0.10/quickstart/#sessions).
   ```
   docker-compose run --rm app ./scripts/generate_flask_key
   ```

   Save the key in the `SESSION_KEY` environment variable in `docker-compose.yml`. Restart the `app` container after
   changing the session key configuration.

3. Run database migrations.
   ```
   docker-compose run --rm app alembic upgrade head
   ```

   This only needs to be run when the containers are created the first time you run `docker-compose up`. Database
   data is persisted by mounting `./pgdata` as PostgreSQL's data directory on the `db` container.

4. Open [http://localhost](http://localhost) in a browser.

## Vagrant

Alternatively, you can launch an instance of the metadata repository in a virtual machine. The VM is
configured to use [PostgreSQL](http://www.postgresql.org/) for the database and
[Apache](https://httpd.apache.org/) with [mod_wsgi](https://modwsgi.readthedocs.io/) for the web server.

**Note**: The VM provision script sets environment variables in `app.wsgi`. Be careful about committing them to
version control.

1. Install VirtualBox and Vagrant

   * [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
   * [Vagrant](http://docs.vagrantup.com/v2/installation/index.html)

2. Launch VM

   ```Shell
   cd /path/to/bdss/metadata_repository
   vagrant up
   ```

3. Open [http://localhost:8000](http://localhost:8000) in a web browser.

   Port 8000 is forwarded to the VM's port 80.

## Manual

To manually set up a development environment, follow these steps:

1. [Install Python 3.4+](http://docs.python-guide.org/en/latest/starting/installation/).

2. Create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

   ```Shell
   cd /path/to/bdss/metadata_repository
   virtualenv -p /path/to/python3 venv
   ```

3. Activate the virtualenv.

   ```Shell
   source venv/bin/activate
   ```

4. Install requirements.

   ```Shell
   pip install -r requirements.txt
   ```

5. Configure the application.

   Two configuration values are read from environment variables:

   * DATABASE_URL - Location of the database to use. See the
     [SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) for more
     information. If you use a path to an SQLite database, it will be automatically created if it doesn't exist.
     For other database types, you may have to install an additional driver.

   * SESSION_KEY - Secret key for [Flask sessions](http://flask.pocoo.org/docs/0.10/quickstart/#sessions). To
     generate a random key, run `./scripts/generate_flask_key`.

6. Create the database schema.

   This project uses [Alembic](https://alembic.readthedocs.org/en/latest/) for database migrations.
   To migrate your database to the latest version, run:

   ```Shell
   alembic upgrade head
   ```

7. Start the development server.

   ```Shell
   ./scripts/serve
   ```

   By default, this server will only be accessible at `localhost`. To make it publicly accessible, run
   the script with the `--public` option.

8. [Configure the client](/client/docs/Configuration.md) to point to your local metadata repository.
