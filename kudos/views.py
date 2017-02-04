from io import BytesIO

import qrcode
from flask import render_template, redirect, url_for, flash, abort, make_response
from flask import send_file

from kudos import app
from kudos import db
from kudos.forms import CreateFeedbackForm
from kudos.models import Feedback, OptionSet, Option, Vote


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/feedback', methods=['GET'])
def all_feedback():
    feedbacks = Feedback.query.all()
    return render_template('feedback_list.html', feedbacks=feedbacks)


@app.route('/feedback/create', methods=['POST', 'GET'])
def create_feedback():
    form = CreateFeedbackForm()
    form.options.choices = [(option.id, option.name) for option in OptionSet.query.all()]
    if form.validate_on_submit():
        option_set = OptionSet.query.get(form.options.data)
        feedback = Feedback(form.name.data, option_set.options, form.description.data)
        db.session.add(feedback)
        db.session.commit()

        img = qrcode.make(url_for('feedback', feedback_id=feedback.id)).get_image().tobytes()
        feedback.qrcode = img
        db.session.add(feedback)
        db.session.commit()
        flash('Created new feedback')
        return redirect(url_for('feedback', feedback_id=feedback.id))
    return render_template('create_feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>', methods=['GET'])
def feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback is None:
        abort(404)
    return render_template('feedback.html', feedback=feedback)


@app.route('/feedback/<int:feedback_id>/<int:option_id>', methods=['GET', 'POST'])
def vote(feedback_id, option_id):
    feedback = Feedback.query.get(feedback_id)

    if feedback is None:
        abort(404)

    option = Option.query.get(option_id)

    if option is None:
        return make_response('Option (id={}) is unknown for this feedback'.format(option_id), 400)

    vote = Vote(feedback.id, option.description)
    db.session.add(vote)
    db.session.commit()

    flash('Thanks for your feedback!')
    return redirect(url_for('feedback', feedback_id=feedback.id))


@app.route('/feedback/<int:feedback_id>/results', methods=['GET'])
def results(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if feedback is None:
        abort(404)

    return render_template('feedback_results.html', feedback=feedback)


@app.route('/feedback/<int:feedback_id>/qrcode', methods=['GET'])
def get_qrcode(feedback_id):
    if feedback is None:
        abort(404)

    img = qrcode.make(url_for('feedback', feedback_id=feedback_id, _external=True))

    img_io = BytesIO()
    img.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')
