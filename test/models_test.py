import unittest

from kudos.models import *


class FeedbackTest(unittest.TestCase):
    def test_convert_to_json(self):
        feeedback = Feedback('some name', [Option('some option')])
        serialized_feedback = feeedback.serialize()
        assert serialized_feedback == {'name': 'some name', 'options': [{'description': 'some option'}]}


class OptionTest(unittest.TestCase):
    def test_convert_to_json(self):
        option = Option('some option')
        assert option.serialize() == {'description': 'some option'}