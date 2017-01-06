from flask import jsonify, abort, request
from flask.views import MethodView

from kudos import app, models


class FeedbackListApi(MethodView):
    def get(self):
        return jsonify({'feedbacks': []})

    def post(self):
        if not request.form:
            abort(400)
        return jsonify({'feedback': ''}), 201


class FeedbackApi(MethodView):
    def get(self, feedback_id):
        abort(404)

    def put(self, feedback_id):
        pass


feedbacklist_view = FeedbackListApi.as_view('feedbacklist_api')
feedback_view = FeedbackApi.as_view('feedback_api')
app.add_url_rule('/api/feedback', view_func=feedbacklist_view, methods=['GET', 'POST',])
app.add_url_rule('/api/feedback/<string:feedback_id>', view_func=feedback_view, methods=['GET', 'PUT', ])
