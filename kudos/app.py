from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from kudos import logger
from raven.contrib.flask import Sentry

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.cfg', silent=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    app.logger.debug(request.form['email'])
    flash('Created new feedback round')
    logger.log('Created new feedback round')
    return redirect(url_for('index'))
