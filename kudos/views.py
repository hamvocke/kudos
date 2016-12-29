from flask import render_template, redirect, url_for, flash, abort

from kudos import app
from kudos import db
from kudos.forms import CreateFeedbackForm
from kudos.models import Feedback, OptionSet


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CreateFeedbackForm()
    form.options.choices = [(option.id, option.name) for option in OptionSet.query.all()]
    if form.validate_on_submit():
        option_set = OptionSet.query.get(form.options.data)
        feedback = Feedback(form.name.data)
        feedback.options = option_set.options
        db.session.add(feedback)
        db.session.commit()
        flash('Created new feedback')
        return redirect(url_for('get_feedback', name=feedback.name))
    return render_template('index.html', form=form)


@app.route('/feedback', methods=['GET'])
def all_feedback():
    feedbacks = Feedback.query.all()
    if len(feedbacks) == 0:
        abort(404)

    return render_template('feedbacks.html', feedbacks=feedbacks)


@app.route('/feedback/<string:name>', methods=['GET'])
def get_feedback(name):
    feedback = Feedback.query.filter_by(name=name).first_or_404()
    return render_template('feedback.html', feedback=feedback)
