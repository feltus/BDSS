#!/usr/bin/env bash

# Provision server for metadata repository

apt-get update

# BDSS dependencies
apt-get install --assume-yes python3-dev libffi-dev

# Install pip dependencies for BDSS
wget "https://bootstrap.pypa.io/get-pip.py"
python3 ./get-pip.py
pip install --requirement /vagrant/requirements.txt

# PostgreSQL
apt-get install --assume-yes postgresql postgresql-contrib

PG_VERSION=$(psql --version | awk '{ print $3 }' | awk 'BEGIN { FS="." } ; { print $1"."$2 }')
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"

# Enable password authentication for bdss database user
sed -i '/local   all             postgres                                peer/i \
local   bdss            bdss                                    md5' "$PG_HBA"

echo "client_encoding = utf8" >> "$PG_CONF"

service postgresql restart

# Create database and user
DB_NAME=bdss
DB_USER=bdss
DB_PASS=bdss

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';

-- Create the database:
CREATE DATABASE $DB_NAME WITH OWNER=$DB_USER
                                 LC_COLLATE='en_US.utf8'
                                 LC_CTYPE='en_US.utf8'
                                 ENCODING='UTF8'
                                 TEMPLATE=template0;
EOF

pip install psycopg2

# Install Apache
apt-get install --assume-yes apache2 apache2-dev

# Install mod_wsgi (apt-get repo version is outdated)
pip install mod_wsgi
/usr/local/bin/mod_wsgi-express install-module
echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi-py34.cpython-34m.so" > /etc/apache2/mods-available/wsgi_express.load
echo "WSGIPythonHome /usr" > /etc/apache2/mods-available/wsgi_express.conf
a2enmod wsgi_express

# Remove default Apache configuration
rm /etc/apache2/sites-enabled/000-default.conf

# Apache configuration for BDSS
cat > /etc/apache2/sites-available/bdss.conf <<EOF

# http://docs.vagrantup.com/v2/synced-folders/virtualbox.html
EnableSendfile Off

<VirtualHost *:80>

    <Directory "/vagrant">
        Require all granted
    </Directory>

    Alias /static/ /vagrant/app/static/

    WSGIDaemonProcess bdss user=www-data group=www-data processes=1 threads=5 \\
        python-path=/usr/local/lib/python3.4/dist-packages:/vagrant
    WSGIScriptAlias / /vagrant/app.wsgi
    WSGIProcessGroup bdss
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On

</VirtualHost>
EOF

ln --symbolic /etc/apache2/sites-available/bdss.conf /etc/apache2/sites-enabled/bdss.conf

# Configuration
# FIXME: Generate configuration variables in app.wsgi
# if [[ ! -e /vagrant/app/app_config.yml ]]; then
#     cd /vagrant
#     cat > app/app_config.yml <<EOF
# database_url: postgresql+psycopg2://bdss:bdss@localhost/bdss
# EOF
#     sh ./scripts/generate_flask_key
# fi

# Create database schema
cd /vagrant
alembic upgrade head

apachectl graceful
