from kudos import app, db
from kudos.models import Feedback, OptionSet, Option, Vote
import unittest


def save_feedback(name, option_set=None):
    feedback = Feedback(name, option_set.options if option_set is not None else [])
    db.session.add(feedback)
    db.session.commit()
    return feedback


def save_option_set(name, options):
    options_to_save = [Option(option) for option in options]

    for option in options_to_save:
        db.session.add(option)

    option_set = OptionSet(name, options_to_save)
    db.session.add(option_set)
    db.session.commit()
    return option_set


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()
        self.option_set = save_option_set('Emoticons', [':(', ':)'])
        self.feedback_dict = dict(email='someMail@example.com', name='test', options=self.option_set.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_render_index_page(self):
        response = self.app.get("/")
        assert response.status_code == 200
        assert b"<h1>Kudos</h1>" in response.data

    def test_should_redirect_to_feedback_page_after_create(self):
        response = self.app.post("/", data=self.feedback_dict, follow_redirects=True)
        assert response.status_code == 200
        assert b"<h1>test</h1>" in response.data

    def test_should_flash_message_after_create(self):
        response = self.app.post("/", data=self.feedback_dict, follow_redirects=True)
        assert b"Created new feedback" in response.data

    def test_should_save_feedback(self):
        self.app.post("/", data=self.feedback_dict, follow_redirects=True)
        saved_feedback = Feedback.query.first()
        assert saved_feedback.name == 'test'
        assert len(saved_feedback.options) == 2

    def test_should_find_all_feedback(self):
        save_feedback('somefeedback')
        save_feedback('anotherfeedback')
        response = self.app.get('/feedback')
        assert response.status_code == 200
        assert b"somefeedback" in response.data
        assert b"anotherfeedback" in response.data

    def test_should_get_single_feedback(self):
        feedback = save_feedback('somefeedback')
        response = self.app.get('/feedback/{}'.format(feedback.id))
        assert response.status_code == 200
        assert b"<h1>somefeedback</h1>" in response.data

    def test_should_return_404_for_unknown_feedback(self):
        response = self.app.get('/feedback/unknown')
        assert response.status_code == 404

    def test_should_flash_message_after_voting(self):
        save_feedback('somefeedback', self.option_set)
        response = self.app.post('/feedback/somefeedback/{}'.format(self.option_set.options[0].id), follow_redirects=True)
        assert response.status_code == 200
        assert b"Thanks for your feedback!" in response.data

    def test_should_return_error_for_invalid_vote(self):
        save_feedback('somefeedback', self.option_set)
        response = self.app.post('/feedback/somefeedback/{}'.format(99))
        assert response.status_code == 400
        assert b"Option (id=99) is unknown for this feedback" in response.data

    def test_should_save_vote(self):
        save_feedback('somefeedback', self.option_set)
        self.app.post('/feedback/somefeedback/{}'.format(self.option_set.options[0].id))
        saved_votes = Vote.query.all()
        assert len(saved_votes) == 1
        assert saved_votes[0].option == ':('

    def test_should_redirect_after_post(self):
        save_feedback('somefeedback', self.option_set)
        response = self.app.post('/feedback/somefeedback/{}'.format(self.option_set.options[0].id))
        assert response.status_code == 302