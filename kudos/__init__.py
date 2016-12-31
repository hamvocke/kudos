import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ.get('APP_PROFILE', 'config.DevelopmentConfig'))
app.config.from_pyfile('config.cfg', silent=True)

db = SQLAlchemy(app)

if not app.debug:
    print('activate logging')
    from raven.contrib.flask import Sentry

    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'], logging=True, level=logging.ERROR)

import kudos.views
import kudos.api
import kudos.models
import kudos.forms
