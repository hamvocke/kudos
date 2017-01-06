import unittest

from flask import json

from kudos import app, db


class RestApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_return_404_for_unknown_feedback(self):
        response = self.app.get('/api/feedback/unknown')
        assert response.status_code == 404

    def test_should_return_list_of_all_feedbacks(self):
        response = self.app.get('/api/feedback')
        assert response.status_code == 200
        assert response.mimetype == 'application/json'
        assert json.loads(response.data) == {'feedbacks': []}

    def test_should_return_400_for_empty_create_request(self):
        response = self.app.post('/api/feedback', data=None)
        assert response.status_code == 400

    def test_should_create_feedback(self):
        feedback = dict(
            name='My Test Feedback',
            options=[1, 2]
        )
        response = self.app.post('/api/feedback', data=feedback)
        assert response.status_code == 201
        assert json.loads(response.data) == {'name': 'My Test Feedback', 'options': []}
