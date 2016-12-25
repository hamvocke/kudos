from kudos import app
from flask import render_template, redirect, url_for, request, flash
from kudos.models import FeedbackRound
from kudos import db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    feedbackRound = FeedbackRound('My awesome feedback session')
    db.session.add(feedbackRound)
    db.session.commit()
    flash('Created new feedback round')
    return redirect(url_for('index'))
