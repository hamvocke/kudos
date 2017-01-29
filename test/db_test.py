from kudos import app, db, models
import unittest

from kudos.models import Vote


def save_feedback(name, option):
    feedback = models.Feedback(name, [option])

    db.session.add(feedback)
    db.session.commit()
    return feedback


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

        save_feedback('some test feedback', some_option)

        saved_feedbacks = models.Feedback.query.all()
        saved_options = models.Option.query.all()
        assert len(saved_feedbacks) == 1
        assert saved_feedbacks[0].name == 'some test feedback'
        assert len(saved_options) == 1
        assert saved_options[0].description == 'some option'

    def test_should_save_creation_time_for_feedback(self):
        some_option = models.Option('some option')
        save_feedback('some test feedback', some_option)
        saved_feedback = models.Feedback.query.first()

        assert saved_feedback.created_at is not None

    def test_should_persist_vote(self):
        some_option = models.Option('some option')
        feedback = save_feedback('some test feedback', some_option)

        self.vote(feedback, some_option)

        saved_votes = models.Vote.query.all()
        assert len(saved_votes) == 1
        assert saved_votes[0].text == 'some text'

    def test_should_save_creation_time_for_vote(self):
        some_option = models.Option('some option')
        feedback = save_feedback('some test feedback', some_option)

        self.vote(feedback, some_option)

        saved_vote = models.Vote.query.first()
        assert saved_vote.created_at is not None

    def vote(self, feedback, some_option):
        vote = Vote(feedback.id, some_option.description, "some text")
        db.session.add(vote)
        db.session.commit()
