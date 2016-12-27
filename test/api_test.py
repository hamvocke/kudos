from kudos import app, db
from kudos.models import FeedbackRound
import unittest

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_return_200_status(self):
        response = self.app.get("/")
        assert response.status_code == 200

    def test_should_render_index_page(self):
        response = self.app.get("/")
        assert b"<h1>Kudos</h1>" in response.data

    def test_should_redirect_to_feedback_page_after_create(self):
        response = self.app.post("/", data=dict(email='someMail@example.com', name='test'), follow_redirects=True)
        assert response.status_code == 200
        assert b"<h1>test</h1>" in response.data

    def test_should_flash_message_after_create(self):
        response = self.app.post("/", data=dict(email='someMail@example.com', name='test'), follow_redirects=True)
        assert b"Created new feedback round" in response.data

    def test_should_save_feedback_round(self):
        response = self.app.post("/", data=dict(email='someMail@example.com', name='test'), follow_redirects=True)
        savedFeedbackRounds = FeedbackRound.query.all()
        assert len(savedFeedbackRounds) == 1
        assert savedFeedbackRounds[0].name == 'test'

    def test_should_find_all_feedback_rounds(self):
        self.saveFeedbackRound('somefeedback')
        self.saveFeedbackRound('anotherfeedback')
        response = self.app.get('/feedback')
        assert response.status_code == 200
        assert b"somefeedback" in response.data
        assert b"anotherfeedback" in response.data

    def test_should_get_single_feedback(self):
        self.saveFeedbackRound('somefeedback')
        response = self.app.get('/feedback/somefeedback')
        assert response.status_code == 200
        assert b"<h1>somefeedback</h1>" in response.data

    def saveFeedbackRound(self, name):
        feedbackRound = FeedbackRound(name)
        db.session.add(feedbackRound)
        db.session.commit()
