from flask import jsonify, abort, request
from flask.views import MethodView

from kudos import app, models, db


class FeedbackListApi(MethodView):
    def get(self):
        return jsonify({'feedbacks': []})

    def post(self):
        if not request.form or not request.form['name']:
            abort(400)

        options = [models.Option.query.get(option_id) for option_id in request.form.getlist('options')]
        if None in options:
            abort(400)

        feedback = models.Feedback(request.form['name'], options)
        db.session.add(feedback)
        db.session.commit()

        return jsonify(feedback.serialize()), 201


class FeedbackApi(MethodView):
    def get(self, feedback_id):
        abort(404)

    def put(self, feedback_id):
        pass


feedbacklist_view = FeedbackListApi.as_view('feedbacklist_api')
feedback_view = FeedbackApi.as_view('feedback_api')
app.add_url_rule('/api/feedback', view_func=feedbacklist_view, methods=['GET', 'POST', ])
app.add_url_rule('/api/feedback/<string:feedback_id>', view_func=feedback_view, methods=['GET', 'PUT', ])
