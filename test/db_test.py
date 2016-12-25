from kudos import app, db, models
import unittest

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_should_persist_feedback_round(self):
        feedbackRound = models.FeedbackRound('some test feedback round')
        db.session.add(feedbackRound)
        db.session.commit()

        savedFeedbackRounds = models.FeedbackRound.query.all()
        assert len(savedFeedbackRounds) == 1
        assert savedFeedbackRounds[0].name == 'some test feedback round'
