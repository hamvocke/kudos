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

    def test_should_persist_feedback(self):
        feedback = models.Feedback('some test feedback')
        db.session.add(feedback)
        db.session.commit()

        savedFeedbacks = models.Feedback.query.all()
        assert len(savedFeedbacks) == 1
        assert savedFeedbacks[0].name == 'some test feedback'
