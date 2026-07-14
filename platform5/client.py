from __future__ import annotations

from platform5.errors import (
    ForbiddenError,
    InsufficientBalanceError,
    NotFoundError,
    Platform5Error,
    RateLimitError,
    UnauthorizedError,
    ValidationError,
)
from platform5.services.account import Account
from platform5.services.email import Email
from platform5.services.messages import Messages
from platform5.services.sms import SMS

import requests


DEFAULT_BASE_URL = "http://localhost:8084"


class HttpClient:
    def __init__(self, api_key: str, base_url: str) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json", "X-API-Key": api_key})

    def request(self, method: str, path: str, json: dict | None = None, idempotency_key: str | None = None) -> dict:
        url = self._base_url + path
        headers: dict[str, str] = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        response = self._session.request(method, url, json=json, headers=headers)
        request_id = response.headers.get("X-Request-ID")
        body = response.json()

        if not response.ok:
            raise _to_error(response.status_code, response.headers, body, request_id)

        return body["data"]


def _to_error(status: int, headers: dict | None, body: dict, request_id: str | None) -> Platform5Error:
    message = body.get("message", "")
    errors = body.get("errors")

    if status == 429:
        limit = int(headers.get("X-RateLimit-Limit", "0")) if headers else 0
        remaining = int(headers.get("X-RateLimit-Remaining", "0")) if headers else 0
        return RateLimitError(status, message, errors, request_id, limit, remaining)

    cls = {
        401: UnauthorizedError,
        402: InsufficientBalanceError,
        403: ForbiddenError,
        404: NotFoundError,
        422: ValidationError,
    }.get(status, Platform5Error)

    return cls(status, message, errors, request_id)


class Platform5:
    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        self._client = HttpClient(api_key, base_url or DEFAULT_BASE_URL)
        self._sms = SMS(self._client)
        self._email = Email(self._client)
        self._messages = Messages(self._client)
        self._account = Account(self._client)

    @property
    def sms(self) -> SMS:
        return self._sms

    @property
    def email(self) -> Email:
        return self._email

    @property
    def messages(self) -> Messages:
        return self._messages

    @property
    def account(self) -> Account:
        return self._account

    def health(self) -> None:
        self._client.request("GET", "/health")
