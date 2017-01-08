import unittest

from kudos.models import *


class FeedbackTest(unittest.TestCase):
    def test_convert_to_json(self):
        option = Option('some option')
        feedback = Feedback('some name', [option])
        feedback.votes = [Vote(feedback.id, option.description)]
        serialized_feedback = feedback.serialize()
        assert serialized_feedback['id'] is None
        assert serialized_feedback['name'] == 'some name'
        assert serialized_feedback['options'][0]['id'] is None
        assert serialized_feedback['options'][0]['description'] == 'some option'
        assert serialized_feedback['votes'][0]['option'] == 'some option'


class OptionTest(unittest.TestCase):
    def test_convert_to_json(self):
        option = Option('some option')
        serialized_option = option.serialize()
        assert serialized_option['id'] is None
        assert serialized_option['description'] == 'some option'


class VoteTest(unittest.TestCase):
    def test_convert_to_json(self):
        feedback = Feedback('some name')
        vote = Vote(feedback.id, 'some vote')
        serialized_vote = vote.serialize()
        assert serialized_vote['option'] == 'some vote'
