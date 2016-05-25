# Code Structure

The metadata repository code is organized into:

* database

   [Alembic](https://alembic.readthedocs.io) configuration and database migrations.

* matchers

   Definitions of available types of [URL Matchers](/metadata_repository/docs/DataModel.md#url-matcher).

* routes

   [Flask](http://flask.pocoo.org/) route handler functions. Generally, each module in this package contains CRUD
   routes for a different type of [data model](/metadata_repository/docs/DataModel.md) object.

* static

   [Static files](http://flask.pocoo.org/docs/latest/quickstart/#static-files) such as JavaScript, CSS, etc.

* templates

   [Templates](http://flask.pocoo.org/docs/0.10/quickstart/#rendering-templates) for rendering UI.

* transfer_mechanisms

   Definitions of available types of [data transfer mechanisms](/metadata_repository/docs/DataModel.md#transfer-mechanism).

* transforms

   Definitions of available types of [URL Transforms](/metadata_repository/docs/DataModel.md#url-matcher#url-transform).

* \_\_init\_\_.py

   Initialization of Flask application.

* core.py

   Core functionality of the metadata repository: identifying alternate URLs for data.

* forms.py

   Definitions of forms.

* models.py

   Definition of [data model](/metadata_repository/docs/DataModel.md) objects.
