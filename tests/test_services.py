import unittest
from unittest.mock import MagicMock, patch

from platform5 import Platform5


def _mock_response(status=200, data=None):
    m = MagicMock()
    m.ok = status >= 200 and status < 300
    m.status_code = status
    m.headers.get.return_value = None
    m.json.return_value = {"success": True, "message": "OK", "data": data or {}}
    return m


class TestSMS(unittest.TestCase):
    @patch("platform5.client.requests.Session.request")
    def test_send(self, mock_request):
        mock_request.return_value = _mock_response(data={
            "message_id": "m1", "to": "+2547", "sender_name": "B",
            "parts": 1, "cost": 1.0, "currency": "KES", "status": "queued",
        })

        app = Platform5(api_key="test")
        resp = app.sms.send(to="+2547", message="Hello", from_="MyBrand")

        self.assertEqual(resp.message_id, "m1")
        self.assertEqual(resp.status, "queued")

    @patch("platform5.client.requests.Session.request")
    def test_send_sends_idempotency_key(self, mock_request):
        mock_request.return_value = _mock_response(data={
            "message_id": "m1", "to": "+2547", "sender_name": "B",
            "parts": 1, "cost": 1.0, "currency": "KES", "status": "queued",
        })

        app = Platform5(api_key="test")
        app.sms.send(to="+2547", message="Hello", from_="MyBrand")

        _, kwargs = mock_request.call_args
        headers = kwargs.get("headers", {})
        self.assertIn("Idempotency-Key", headers)
        self.assertTrue(len(headers["Idempotency-Key"]) > 0)


class TestEmail(unittest.TestCase):
    @patch("platform5.client.requests.Session.request")
    def test_send(self, mock_request):
        mock_request.return_value = _mock_response(data={
            "message_id": "e1", "status": "queued",
        })

        app = Platform5(api_key="test")
        resp = app.email.send(to="a@b.com", subject="Hi", body="Hello", from_="MyBrand")

        self.assertEqual(resp.message_id, "e1")

    @patch("platform5.client.requests.Session.request")
    def test_send_with_html(self, mock_request):
        mock_request.return_value = _mock_response(data={
            "message_id": "e1", "status": "queued",
        })

        app = Platform5(api_key="test")
        app.email.send(to="a@b.com", subject="Hi", body="<h1>Hello</h1>", from_="MyBrand", body_type="html")

        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["json"]["body_type"], "html")


class TestMessages(unittest.TestCase):
    @patch("platform5.client.requests.Session.request")
    def test_get(self, mock_request):
        mock_request.return_value = _mock_response(data={
            "id": "m1", "to": "+2547", "sender_name": "B",
            "parts": 1, "cost": 1.0, "status": "delivered",
            "created_at": "2024-01-01T00:00:00Z",
        })

        app = Platform5(api_key="test")
        resp = app.messages.get("m1")

        self.assertEqual(resp.id, "m1")
        self.assertEqual(resp.status, "delivered")


class TestAccount(unittest.TestCase):
    @patch("platform5.client.requests.Session.request")
    def test_get_balance(self, mock_request):
        mock_request.return_value = _mock_response(data={
            "available_balance": 1250.50, "current_balance": 1500.00, "currency": "KES",
        })

        app = Platform5(api_key="test")
        resp = app.account.get_balance()

        self.assertEqual(resp.available_balance, 1250.50)
        self.assertEqual(resp.currency, "KES")


if __name__ == "__main__":
    unittest.main()
