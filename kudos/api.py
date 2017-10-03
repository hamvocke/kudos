from flask import jsonify, abort, request
from flask.views import MethodView

from kudos import app, models, db


class FeedbackListApi(MethodView):
    def get(self):
        feedback_list = models.Feedback.query.all()
        return jsonify({'feedback': [feedback.serialize() for feedback in feedback_list]})

    def post(self):
        if not request.form or not request.form['name']:
            abort(400, 'no feedback data provided')

        options = [models.Option.query.get(option_id) for option_id in request.form.getlist('options')]
        if None in options:
            abort(400, 'invalid option')

        feedback = models.Feedback(request.form['name'], options, request.form['description'])
        db.session.add(feedback)
        db.session.commit()

        return jsonify(feedback.serialize()), 201


class FeedbackApi(MethodView):
    def get(self, feedback_id):
        feedback = models.Feedback.query.get(feedback_id)

        if feedback is None:
            abort(404)

        return jsonify(feedback.serialize())

    def put(self, feedback_id):
        pass


class VoteApi(MethodView):
    def post(self, feedback_id):
        if not request.form or not request.form['option']:
            abort(400, 'no vote option provided')

        feedback = models.Feedback.query.get(feedback_id)
        option = models.Option.query.get(request.form['option'])

        if feedback is None:
            abort(404, 'feedback with id {} not found'.format(feedback_id))

        if option is None:
            abort(404, 'option with id {} not found'.format(request.form['option']))

        vote = models.Vote(feedback.id, option.description)
        feedback.votes.append(vote)
        db.session.add(feedback)
        db.session.commit()

        return jsonify({}), 201


feedbacklist_view = FeedbackListApi.as_view('feedbacklist_api')
feedback_view = FeedbackApi.as_view('feedback_api')
vote_view = VoteApi.as_view('vote_api')
app.add_url_rule('/api/feedback', view_func=feedbacklist_view, methods=['GET', 'POST', ])
app.add_url_rule('/api/feedback/<string:feedback_id>', view_func=feedback_view, methods=['GET', 'PUT', ])
app.add_url_rule('/api/feedback/<string:feedback_id>/vote', view_func=vote_view, methods=['POST', ])
