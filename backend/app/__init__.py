from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler

from config import app_config

db = SQLAlchemy()
logger = None

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    # register config files
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # initialize database ORM
    db.init_app(app)

    migrate = Migrate(app, db)
    from app import models

    # add logging
    handler = RotatingFileHandler(config_name + '.log', maxBytes=10000, backupCount=1)
    app.logger.addHandler(handler)
    global logger
    logger = app.logger

    # add blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app