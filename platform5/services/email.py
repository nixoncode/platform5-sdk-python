from uuid import uuid4

from platform5.types import SendEmailResponse


class Email:
    def __init__(self, client) -> None:
        self._client = client

    def send(self, to: str, subject: str, body: str, from_: str, body_type: str | None = None) -> SendEmailResponse:
        payload = {"to": to, "subject": subject, "body": body, "from": from_}
        if body_type:
            payload["body_type"] = body_type
        data = self._client.request("POST", "/v1/email/send", json=payload, idempotency_key=str(uuid4()))
        return SendEmailResponse(**data)
