from io import BytesIO

from flask import render_template, redirect, url_for, flash, abort, send_file

from kudos import app
from kudos import db
from kudos import qr
from kudos.forms import CreateFeedbackForm, VoteForm
from kudos.models import Feedback, Option


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
    form.options.choices = [(option.id, option.description) for option in Option.query.all()]
    if form.validate_on_submit():
        options = [Option.query.get(option_id) for option_id in form.options.data]
        feedback = Feedback(form.name.data, options, form.description.data)
        db.session.add(feedback)
        db.session.commit()

        feedback.qrcode = qr.create_qr_code(feedback.id)
        db.session.add(feedback)
        db.session.commit()

        flash('Created new feedback')
        return redirect(url_for('created_feedback', feedback_id=feedback.id))
    return render_template('create_feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/start', methods=['GET'])
def created_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback is None:
        abort(404)
    return render_template('created_feedback.html')


@app.route('/feedback/<int:feedback_id>/kiosk', methods=['GET'])
def feedback_kiosk(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback is None:
        abort(404)
    return render_template('feedback_kiosk.html', feedback=feedback)


@app.route('/feedback/<int:feedback_id>', methods=['GET', 'POST'])
def feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback is None:
        abort(404)

    form = VoteForm()
    form.option.choices = [(option.id, option.description) for option in feedback.options]

    if form.validate_on_submit():
        option_id = form.option.data
        text = form.text.data

        option = Option.query.get(option_id)

        feedback.vote(option, text)
        db.session.add(feedback)
        db.session.commit()

        flash('Thanks for your feedback!')
        return redirect(url_for('feedback', feedback_id=feedback.id))

    return render_template('feedback.html', feedback=feedback, form=form)


@app.route('/feedback/<int:feedback_id>/results', methods=['GET'])
def results(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if feedback is None:
        abort(404)

    return render_template('feedback_results.html', feedback=feedback)


@app.route('/feedback/<int:feedback_id>/qrcode', methods=['GET'])
def get_qrcode(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if feedback is None:
        abort(404)

    return send_file(BytesIO(feedback.qrcode), mimetype='image/jpeg')
