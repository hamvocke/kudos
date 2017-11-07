import unittest

from kudos import app, db
from kudos.models import Feedback, Option, Vote


def save_feedback(name, options=[], description=None):
    feedback = Feedback(name, options, description)
    db.session.add(feedback)
    db.session.commit()
    return feedback


def save_options(options):
    options_to_save = [Option(option) for option in options]

    for option in options_to_save:
        db.session.add(option)

    db.session.commit()
    return options_to_save


class ViewTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()
        self.options = save_options([':(', ':)'])
        self.feedback_dict = dict(email='someMail@example.com', name='test', options=self.options[0].id,
                                  description='some description')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_render_index_page(self):
        response = self.app.get("/")

        assert response.status_code == 200
        assert b"<h1>Kudos</h1>" in response.data

    def test_should_render_frontpage(self):
        response = self.app.get("/frontpage")

        assert response.status_code == 200

    def test_should_render_create_feedback_page(self):
        response = self.app.get("/feedback/create")

        assert response.status_code == 200
        assert b"Get your feedback. It's super simple!" in response.data

    def test_should_redirect_to_feedback_created_page_after_create(self):
        response = self.app.post("/feedback/create", data=self.feedback_dict, follow_redirects=True)

        assert response.status_code == 200
        assert b"<h2>You're ready for feedback!</h2>" in response.data

    def test_should_show_getting_started_page(self):
        feedback = save_feedback('somefeedback', self.options)

        response = self.app.get("/feedback/{}/start".format(feedback.id))

        assert response.status_code == 200
        assert b"<h2>You're ready for feedback!</h2>" in response.data

    def test_should_show_404_on_getting_started_page(self):
        response = self.app.get("/feedback/999/start")

        assert response.status_code == 404

    def test_should_flash_message_after_create(self):
        response = self.app.post("/feedback/create", data=self.feedback_dict, follow_redirects=True)

        assert b"Created new feedback" in response.data

    def test_should_save_feedback(self):
        self.app.post("/feedback/create", data=self.feedback_dict, follow_redirects=True)

        saved_feedback = Feedback.query.first()
        assert saved_feedback.name == 'test'
        assert saved_feedback.description == 'some description'
        assert len(saved_feedback.options) == 1

    def test_should_find_all_feedback(self):
        save_feedback('somefeedback')
        save_feedback('anotherfeedback')

        response = self.app.get('/feedback')

        assert response.status_code == 200
        assert b"somefeedback" in response.data
        assert b"anotherfeedback" in response.data

    def test_should_show_empty_page_if_no_feedback_present(self):
        response = self.app.get('/feedback')

        assert response.status_code == 200
        assert b"There seems to be nothing here yet" in response.data

    def test_should_show_feedback_page(self):
        feedback = save_feedback('somefeedback', options=self.options, description='some description')

        response = self.app.get('/feedback/{}'.format(feedback.id))

        assert response.status_code == 200
        assert b"<h2>somefeedback</h2>" in response.data
        assert b"some description" in response.data
        assert b":)" in response.data
        assert b":(" in response.data

    def test_should_show_kiosk_feedback_page(self):
        feedback = save_feedback('somefeedback', options=self.options, description='some description')

        response = self.app.get('/feedback/{}/kiosk'.format(feedback.id))

        assert response.status_code == 200
        assert b"<h2>somefeedback</h2>" in response.data
        assert b"some description" in response.data
        assert b":)" in response.data
        assert b":(" in response.data

    def test_should_return_404_for_unknown_feedback(self):
        response = self.app.get('/feedback/100')

        assert response.status_code == 404

    def test_should_flash_message_after_voting(self):
        feedback = save_feedback('somefeedback', self.options)
        vote = {
            'option': self.options[0].id,
            'text': 'some text'
        }

        response = self.app.post('/feedback/{}'.format(feedback.id), data=vote, follow_redirects=True)

        assert response.status_code == 200
        assert b"Thanks for your feedback!" in response.data

    def test_should_save_vote(self):
        feedback = save_feedback('somefeedback', self.options)
        vote = {
            'option': self.options[0].id,
            'text': 'some text'
        }

        self.app.post('/feedback/{}'.format(feedback.id), data=vote, follow_redirects=True)

        saved_votes = Vote.query.all()
        assert len(saved_votes) == 1
        assert saved_votes[0].option == ':('

    def test_should_redirect_after_vote(self):
        feedback = save_feedback('somefeedback', self.options)
        vote = {
            'option': self.options[0].id,
            'text': 'some text'
        }

        response = self.app.post('/feedback/{}'.format(feedback.id), data=vote)

        assert response.status_code == 302

    def test_should_show_feedback_results(self):
        feedback = save_feedback('somefeedback', self.options)

        response = self.app.get('/feedback/{}/results'.format(feedback.id))

        expected_body = "Your feedback for '<em>{}</em>'".format(feedback.name)
        assert response.status_code == 200
        assert expected_body in response.data.decode('utf-8')

    def test_should_return_404_for_unknown_feedback_results(self):
        response = self.app.get('/feedback/{}/results'.format('100'))

        assert response.status_code == 404

    def test_should_serve_qrcode_image(self):
        self.app.post("/feedback/create", data=self.feedback_dict, follow_redirects=True)

        response = self.app.get('/feedback/{}/qrcode'.format('1'))

        assert response.status_code == 200
        assert len(response.data) > 0
        assert response.mimetype == 'image/jpeg'

    def test_should_return_404_for_unknown_feedback_qrcode(self):
        response = self.app.get('/feedback/{}/qrcode'.format('100'))
        assert response.status_code == 404
