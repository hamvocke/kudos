from kudos import app
from flask import render_template, redirect, url_for, request, flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    app.logger.debug(request.form['email'])
    flash('Created new feedback round')
    app.logger.error('this should show up in sentry')
    return redirect(url_for('index'))
