import unittest

from kudos.models import *


class FeedbackTest(unittest.TestCase):
    def test_convert_to_json(self):
        feeedback = Feedback('some name', [Option('some option')])
        serialized_feedback = feeedback.serialize()
        assert serialized_feedback['id'] is None
        assert serialized_feedback['name'] == 'some name'
        assert serialized_feedback['options'][0]['id'] is None
        assert serialized_feedback['options'][0]['description'] == 'some option'


class OptionTest(unittest.TestCase):
    def test_convert_to_json(self):
        option = Option('some option')
        serialized_option = option.serialize()
        assert serialized_option['id'] is None
        assert serialized_option['description'] == 'some option'
