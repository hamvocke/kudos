from flask import jsonify, abort
from flask.views import MethodView

from kudos import app


class FeedbackApi(MethodView):
    def get(self, feedback_id):
        if feedback_id is None:
            return jsonify({'feedbacks': []})
        else:
            abort(404)

    def post(self):
        pass

    def put(self, feedback_id):
        pass


feedback_view = FeedbackApi.as_view('feedback_api')
app.add_url_rule('/api/feedback/', defaults={'feedback_id': None}, view_func=feedback_view, methods=['GET', ])
app.add_url_rule('/api/feedback/', view_func=feedback_view, methods=['POST', ])
app.add_url_rule('/api/feedback/<string:feedback_id>', view_func=feedback_view, methods=['GET', 'PUT', ])
