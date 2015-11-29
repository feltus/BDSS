from flask import Flask

from .config import app_config
from .models import db_session
from .routes import routes

app = Flask(__name__)
app.secret_key = app_config["secret_key"]


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Close DB session when app shuts down
    http://flask.pocoo.org/docs/0.10/patterns/sqlalchemy/#declarative
    """
    db_session.remove()


app.register_blueprint(routes)
