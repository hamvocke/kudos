from flask import Flask
import logging
from raven.contrib.flask import Sentry
from kudos.database import db_session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.cfg', silent=True)

if not app.debug:
    print('activate logging')
    from raven.contrib.flask import Sentry
    sentry = Sentry(app, dsn=app.config['SENTRY_DSN'], logging=True, level=logging.ERROR)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import kudos.views
