import unittest
from unittest.mock import MagicMock, patch

from platform5 import Platform5


class TestPlatform5(unittest.TestCase):
    def test_creates_client(self):
        app = Platform5(api_key="test-key")
        self.assertIsNotNone(app)
        self.assertIsNotNone(app.sms)
        self.assertIsNotNone(app.email)
        self.assertIsNotNone(app.messages)
        self.assertIsNotNone(app.account)

    def test_default_base_url(self):
        app = Platform5(api_key="test-key")
        self.assertEqual(app._client._base_url, "http://localhost:8084")

    def test_custom_base_url(self):
        app = Platform5(api_key="test-key", base_url="http://example.com")
        self.assertEqual(app._client._base_url, "http://example.com")


class TestHealth(unittest.TestCase):
    @patch("platform5.client.requests.Session.request")
    def test_health_ok(self, mock_request):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "message": "OK", "data": None}
        mock_request.return_value = mock_response

        app = Platform5(api_key="test-key")
        app.health()  # should not raise

    @patch("platform5.client.requests.Session.request")
    def test_health_failure(self, mock_request):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 401
        mock_response.headers.get.return_value = None
        mock_response.json.return_value = {"success": False, "message": "Unauthorized", "errors": "bad key"}
        mock_request.return_value = mock_response

        app = Platform5(api_key="bad-key")
        with self.assertRaises(Exception):
            app.health()


class TestAuthHeader(unittest.TestCase):
    def test_sends_api_key(self):
        app = Platform5(api_key="p5_test_key")
        session_headers = app._client._session.headers
        self.assertEqual(session_headers.get("X-API-Key"), "p5_test_key")


if __name__ == "__main__":
    unittest.main()
