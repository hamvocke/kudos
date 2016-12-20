from flask import Flask
import logging
from raven.contrib.flask import Sentry


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.cfg', silent=True)

if not app.debug:
    from raven.contrib.flask import Sentry
    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'], logging=True, level=logging.ERROR)

import kudos.views
