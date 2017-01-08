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

    def test_should_return_single_feedback(self):
        option = self.create_option('some option')
        created_feedback = self.create_feedback('some-feedback', [option])

        response = self.app.get('/api/feedback/{}'.format(created_feedback['id']))
        assert response.status_code == 200

    def test_should_return_list_of_all_feedbacks(self):
        response = self.app.get('/api/feedback')
        assert response.status_code == 200
        assert response.mimetype == 'application/json'
        assert json.loads(response.data) == {'feedbacks': []}

    def test_should_return_400_for_empty_create_request(self):
        response = self.app.post('/api/feedback', data=None)
        assert response.status_code == 400

    def test_should_return_400_for_unknown_option_in_create_request(self):
        feedback = {
            'name': 'My Test Feedback',
            'options': [-1]
        }
        response = self.app.post('/api/feedback', data=feedback)
        assert response.status_code == 400

    def test_should_create_feedback(self):
        option1 = self.create_option('some option')
        option2 = self.create_option('another option')
        feedback = {
            'name': 'My Test Feedback',
            'options': [option1.id, option2.id]
        }

        response = self.app.post('/api/feedback', data=feedback)

        parsed_response = json.loads(response.data)
        assert response.status_code == 201
        assert parsed_response['id'] is not None
        assert parsed_response['name'] == 'My Test Feedback'
        assert len(parsed_response['options']) == 2

    def create_feedback(self, name, options):
        feedback = {
            'name': name,
            'options': [option.id for option in options]
        }

        response = self.app.post('/api/feedback', data=feedback)
        return json.loads(response.data)

    def create_option(self, description):
        option = models.Option(description)
        db.session.add(option)
        db.session.commit()
        return option
