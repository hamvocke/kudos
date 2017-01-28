import unittest

from flask import json

from kudos import app, db, models


def create_option(description):
    option = models.Option(description)
    db.session.add(option)
    db.session.commit()
    return option


def create_feedback(name, options, votes=[], description=None):
    feedback = models.Feedback(name, options, description)
    if len(votes) > 0:
        feedback.votes = [models.Vote(feedback.id, vote.description) for vote in votes]
    db.session.add(feedback)
    db.session.commit()
    return feedback


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
        option = create_option('some option')
        created_feedback = create_feedback('some-feedback', [option], [option], 'some description')

        response = self.app.get('/api/feedback/{}'.format(created_feedback.id))
        parsed_response = json.loads(response.data)
        assert response.status_code == 200
        assert parsed_response == {
            'id': 1,
            'name': 'some-feedback',
            'description': 'some description',
            'options': [
                {
                    'id': 1,
                    'description': 'some option'
                }
            ],
            'votes': [
                {'option': 'some option'}
            ]
        }

    def test_should_return_feedback_list(self):
        option = create_option('some option')
        some_feedback = create_feedback('some feedback', [option])
        another_feedback = create_feedback('another feedback', [option])

        response = self.app.get('/api/feedback')

        assert response.status_code == 200
        assert response.mimetype == 'application/json'
        assert json.loads(response.data) == {
            'feedbacks': [
                some_feedback.serialize(),
                another_feedback.serialize()
            ]
        }

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
        option1 = create_option('some option')
        option2 = create_option('another option')
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

    def test_should_vote_on_feedback(self):
        option = create_option('some option')
        feedback = create_feedback('soome feedback', [option])

        vote_data = {'option': option.id}
        response = self.app.post('/api/feedback/{}/vote'.format(feedback.id), data=vote_data)

        assert response.status_code == 201

    def test_should_save_vote_on_feedback(self):
        option = create_option('some option')
        feedback = create_feedback('some feedback', [option])
        feedback_id = feedback.id

        vote_data = {'option': option.id}
        self.app.post('/api/feedback/{}/vote'.format(feedback.id), data=vote_data)

        vote = models.Vote.query.filter_by(feedback_id=feedback_id).first()
        assert vote is not None

    def test_should_return_404_on_unknown_vote_option(self):
        option = create_option('some option')
        feedback = create_feedback('soome feedback', [option])

        vote_data = {'option': 99}
        response = self.app.post('/api/feedback/{}/vote'.format(feedback.id), data=vote_data)

        assert response.status_code == 404

    def test_should_return_400_on_missing_vote_option(self):
        option = create_option('some option')
        feedback = create_feedback('soome feedback', [option])

        response = self.app.post('/api/feedback/{}/vote'.format(feedback.id), data=None)

        assert response.status_code == 400
