from uuid import uuid4

from platform5.types import SendSMSResponse


class SMS:
    def __init__(self, client) -> None:
        self._client = client

    def send(self, to: str, message: str, from_: str) -> SendSMSResponse:
        data = self._client.request("POST", "/v1/sms/send", json={"to": to, "message": message, "from": from_}, idempotency_key=str(uuid4()))
        return SendSMSResponse(**data)
