from kudos import app
from flask import render_template, redirect, url_for, request, flash, abort
from flask.views import MethodView
from kudos.models import FeedbackRound
from kudos.forms import CreateFeedbackForm
from kudos import db

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CreateFeedbackForm()
    if form.validate_on_submit():
        feedbackRound = FeedbackRound(form.name.data)
        db.session.add(feedbackRound)
        db.session.commit()
        flash('Created new feedback round')
        return redirect(url_for('get_feedback', name=feedbackRound.name))
    return render_template('index.html', form=form)

@app.route('/feedback', methods=['GET'])
def all_feedback():
    feedbacks = FeedbackRound.query.all()
    if len(feedbacks) == 0:
        abort(404)

    return render_template('feedbacks.html', feedbacks = feedbacks)

@app.route('/feedback/<string:name>', methods=['GET'])
def get_feedback(name):
    feedback = FeedbackRound.query.filter_by(name=name).first_or_404()
    return render_template('feedback.html', feedback = feedback)
