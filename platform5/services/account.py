from platform5.types import BalanceResponse


class Account:
    def __init__(self, client) -> None:
        self._client = client

    def get_balance(self) -> BalanceResponse:
        data = self._client.request("GET", "/v1/balance")
        return BalanceResponse(**data)
