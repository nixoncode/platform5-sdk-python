from platform5.types import MessageStatusResponse


class Messages:
    def __init__(self, client) -> None:
        self._client = client

    def get(self, id: str) -> MessageStatusResponse:
        data = self._client.request("GET", f"/v1/messages/{id}")
        return MessageStatusResponse(**data)
