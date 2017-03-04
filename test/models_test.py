import unittest

from freezegun import freeze_time

from kudos.models import *


class FeedbackTest(unittest.TestCase):
    @freeze_time('2017-01-01')
    def test_convert_to_json(self):
        option = Option('some option')
        feedback = Feedback('some name', [option], 'some description', ends_at=arrow.utcnow())
        feedback.votes = [Vote(feedback.id, option.description)]
        serialized_feedback = feedback.serialize()
        assert serialized_feedback['id'] is None
        assert serialized_feedback['name'] == 'some name'
        assert serialized_feedback['description'] == 'some description'
        assert serialized_feedback['created_at'] is not None
        assert serialized_feedback['ends_at'] == '2017-01-01T00:00:00+00:00'
        assert serialized_feedback['options'][0]['id'] is None
        assert serialized_feedback['options'][0]['description'] == 'some option'
        assert serialized_feedback['votes'][0]['option'] == 'some option'
        assert serialized_feedback['votes'][0]['created_at'] == '2017-01-01T00:00:00+00:00'

    def test_status_closed(self):
        option = Option('some option')
        yesterday = arrow.utcnow().replace(days=-1)
        feedback = Feedback('some name', [option], 'some description', ends_at=yesterday)
        assert feedback.status() == FeedbackStatus.CLOSED

    def test_status_active(self):
        option = Option('some option')
        tomorrow = arrow.utcnow().replace(days=+1)
        feedback = Feedback('some name', [option], 'some description', ends_at=tomorrow)
        assert feedback.status() == FeedbackStatus.ACTIVE

    def test_vote(self):
        options = [Option('some option'), Option('another option')]
        feedback = Feedback('some name', options)
        feedback.vote(options[0], 'some text')

        assert len(feedback.votes) == 1
        assert feedback.votes[0].option == 'some option'
        assert feedback.votes[0].text == 'some text'

    def test_aggregate_votes(self):
        options = [Option('some option'), Option('another option')]
        feedback = Feedback('some name', options)
        feedback.votes = [Vote(feedback.id, options[0].description),
                          Vote(feedback.id, options[0].description),
                          Vote(feedback.id, options[1].description)]

        assert feedback.aggregate_votes() == {'some option': 2,
                                              'another option': 1}


class OptionTest(unittest.TestCase):
    def test_convert_to_json(self):
        option = Option('some option')
        serialized_option = option.serialize()
        assert serialized_option['id'] is None
        assert serialized_option['description'] == 'some option'


class VoteTest(unittest.TestCase):
    @freeze_time('2017-01-01')
    def test_convert_to_json(self):
        feedback = Feedback('some name')
        vote = Vote(feedback.id, 'some vote')
        serialized_vote = vote.serialize()
        assert serialized_vote['option'] == 'some vote'
        assert serialized_vote['created_at'] == '2017-01-01T00:00:00+00:00'
