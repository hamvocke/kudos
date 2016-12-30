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
        some_option = models.Option('some option')
        feedback = models.Feedback('some test feedback', [some_option])
        db.session.add(feedback)
        db.session.commit()

        saved_feedbacks = models.Feedback.query.all()
        saved_options = models.Option.query.all()
        assert len(saved_feedbacks) == 1
        assert saved_feedbacks[0].name == 'some test feedback'
        assert len(saved_options) == 1
        assert saved_options[0].description == 'some option'
