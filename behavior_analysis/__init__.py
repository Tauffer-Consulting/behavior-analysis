from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os


db_file_path = Path(__file__).resolve().parent / 'database.db'
if os.path.exists(db_file_path):
    os.remove(db_file_path)
    print('\nExisting database removed. New Database created.')

db = SQLAlchemy()


def init_app():
    """Core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.ConfigDev')

    db.init_app(app)

    with app.app_context():
        from . import routes

        # Register applications
        from .apps import init_app_home
        app = init_app_home(app)

        return app
