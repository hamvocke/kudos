from kudos import app
from flask import render_template, redirect, url_for, request, flash, abort
from flask.views import MethodView
from kudos.models import FeedbackRound
from kudos import db

@app.route('/')
def index():
    return render_template('index.html')

class FeedbackRoundApi(MethodView):
    def get(self, name):
        if name is None:
            feedbackRounds = FeedbackRound.query.all()
        else:
            feedbackRounds = FeedbackRound.query.filter_by(name=name).all()

        if len(feedbackRounds) == 0:
            abort(404)

        return render_template('feedbacks.html', feedbackRounds = feedbackRounds)

    def post(self):
        name = request.form['name']
        if name is None:
            name = 'awesome feedback'
        feedbackRound = FeedbackRound(name)
        db.session.add(feedbackRound)
        db.session.commit()
        flash('Created new feedback round')
        return redirect(url_for('feedback_api', name=feedbackRound.name))

    def put(self, name):
        pass

feedbackRoundView = FeedbackRoundApi.as_view('feedback_api')
app.add_url_rule('/feedback/', defaults={'name': None}, view_func=feedbackRoundView, methods=['GET',])
app.add_url_rule('/feedback/', view_func=feedbackRoundView, methods=['POST'])
app.add_url_rule('/feedback/<string:name>', view_func=feedbackRoundView, methods=['GET', 'PUT'])
