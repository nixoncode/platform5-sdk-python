import unittest
from unittest.mock import MagicMock, patch

from platform5 import Platform5
from platform5.errors import (
    UnauthorizedError,
    InsufficientBalanceError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)


class TestErrors(unittest.TestCase):
    def _mock_error(self, status, headers=None):
        m = MagicMock()
        m.ok = False
        m.status_code = status
        m.headers.get = lambda k, d=None: (headers or {}).get(k, d)
        m.json.return_value = {"success": False, "message": "Error", "errors": "detail"}
        return m

    @patch("platform5.client.requests.Session.request")
    def test_401(self, mock_request):
        mock_request.return_value = self._mock_error(401)
        app = Platform5(api_key="bad")
        with self.assertRaises(UnauthorizedError):
            app.health()

    @patch("platform5.client.requests.Session.request")
    def test_402(self, mock_request):
        mock_request.return_value = self._mock_error(402)
        app = Platform5(api_key="test")
        with self.assertRaises(InsufficientBalanceError):
            app.health()

    @patch("platform5.client.requests.Session.request")
    def test_403(self, mock_request):
        mock_request.return_value = self._mock_error(403)
        app = Platform5(api_key="test")
        with self.assertRaises(ForbiddenError):
            app.health()

    @patch("platform5.client.requests.Session.request")
    def test_404(self, mock_request):
        mock_request.return_value = self._mock_error(404)
        app = Platform5(api_key="test")
        with self.assertRaises(NotFoundError):
            app.health()

    @patch("platform5.client.requests.Session.request")
    def test_422(self, mock_request):
        mock_request.return_value = self._mock_error(422)
        app = Platform5(api_key="test")
        with self.assertRaises(ValidationError):
            app.health()

    @patch("platform5.client.requests.Session.request")
    def test_429(self, mock_request):
        mock_request.return_value = self._mock_error(429, {"X-RateLimit-Limit": "50", "X-RateLimit-Remaining": "0"})
        app = Platform5(api_key="test")
        with self.assertRaises(RateLimitError) as ctx:
            app.health()
        self.assertEqual(ctx.exception.limit, 50)
        self.assertEqual(ctx.exception.remaining, 0)


if __name__ == "__main__":
    unittest.main()
