import unittest

from flask import json

from kudos import app, db, models


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
        option1 = self.create_option('some option')
        option2 = self.create_option('another option')

        feedback = {
            'name': 'My Test Feedback',
            'options': [option1.id, option2.id]
        }
        response = self.app.post('/api/feedback', data=feedback)
        assert response.status_code == 201
        assert json.loads(response.data) == {
            'name': 'My Test Feedback',
            'options': [
                {'description': 'some option'},
                {'description': 'another option'}
            ]
        }

    def create_option(self, description):
        option = models.Option(description)
        db.session.add(option)
        db.session.commit()
        return option
