from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from raven.contrib.flask import Sentry

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('production.py')

sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    app.logger.debug(request.form['email'])
    flash('Created new feedback round')
    sentry.captureMessage('Created new feedback round')
    return redirect(url_for('index'))
