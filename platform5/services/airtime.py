from uuid import uuid4

from platform5.types import BuyAirtimeResponse


class Airtime:
    def __init__(self, client) -> None:
        self._client = client

    def buy(self, phone_number: str, amount: float) -> BuyAirtimeResponse:
        data = self._client.request(
            "POST",
            "/v1/airtime/buy",
            json={"phone_number": phone_number, "amount": amount},
            idempotency_key=str(uuid4()),
        )
        return BuyAirtimeResponse(**data)
