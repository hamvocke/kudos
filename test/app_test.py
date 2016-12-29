import unittest
from unittest.mock import patch

from kudos import initial_data


class AppTestCase(unittest.TestCase):
    @patch('kudos.initial_data.db')
    @patch('kudos.initial_data.models.Option.query')
    def test_should_save_options_if_not_present(self, mock_query, mock_db):
        mock_query.all.return_value = []
        initial_data.init_db()
        assert mock_db.session.add.called is True
        assert mock_db.session.commit.called is True

    @patch('kudos.initial_data.db')
    @patch('kudos.initial_data.models.Option.query')
    def test_should_do_nothing_if_options_are_present(self, mock_query, mock_db):
        mock_query.all.return_value = ['something']
        initial_data.init_db()
        assert mock_db.session.add.called is False
        assert mock_db.session.commit.called is False