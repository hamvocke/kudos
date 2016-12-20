from kudos import app
import unittest

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_should_return_200_status(self):
        response = self.app.get("/")
        assert response.status_code == 200

    def test_should_render_index_page(self):
        response = self.app.get("/")
        assert b"<h1>Kudos</h1>" in response.data

    def test_should_redirect_to_index_after_create(self):
        response = self.app.post("/create", data=dict(email='someMail@example.com'), follow_redirects=True)
        assert response.status_code == 200
        assert b"<h1>Kudos</h1>" in response.data

    def test_should_flash_message_after_create(self):
        response = self.app.post("/create", data=dict(email='someMail@example.com'), follow_redirects=True)
        assert b"Created new feedback round" in response.data
