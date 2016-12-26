from kudos import app
from flask import render_template, redirect, url_for, request, flash
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

        if feedbackRounds is None:
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
        return redirect(url_for('feedbackRound', name=feedbackRound.name))

feedbackRoundView = FeedbackRoundApi.as_view('feedbackRound')
app.add_url_rule('/feedbackRound/', defaults={'name': None}, view_func=feedbackRoundView, methods=['GET'])
app.add_url_rule('/feedbackRound/', view_func=feedbackRoundView, methods=['POST'])
app.add_url_rule('/feedbackRound/<string:name>', view_func=feedbackRoundView, methods=['GET'])
