# platform5-sdk

Python SDK for the Platform5 Developer API.

## Install

```sh
pip install platform5-sdk
```

## Usage

```python
from platform5 import Platform5

client = Platform5(api_key="p5_live_abc123def456")

# Send an SMS
resp = client.sms.send(
    to="+254712345678",
    message="Your appointment is confirmed for tomorrow at 10 AM.",
    from_="MyBrand",
)
print(resp.message_id, resp.parts, resp.cost)

# Send an email
client.email.send(
    to="user@example.com",
    subject="Welcome to Platform5",
    body="Hello, thank you for signing up!",
    from_="MyBrand",
)

# Check message status
status = client.messages.get("msg-uuid")
print(status.status)

# Check balance
balance = client.account.get_balance()
print(balance.available_balance, balance.currency)
```

## Configuration

```python
Platform5(
    api_key="p5_live_abc123",
    base_url="http://localhost:8084",  # optional, defaults to http://localhost:8084
)
```

## Services

| Method | Endpoint |
|--------|----------|
| `client.sms.send(to, message, from_)` | POST /v1/sms/send |
| `client.email.send(to, subject, body, from_, body_type?)` | POST /v1/email/send |
| `client.messages.get(id)` | GET /v1/messages/{id} |
| `client.account.get_balance()` | GET /v1/balance |
| `client.health()` | GET /health |

## Error Handling

```python
from platform5.errors import (
    UnauthorizedError,
    InsufficientBalanceError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    Platform5Error,
)

try:
    client.sms.send(to="+2547", message="Hello", from_="MyBrand")
except RateLimitError as e:
    print(f"Rate limited: {e.remaining}/{e.limit}")
except Platform5Error as e:
    print(f"API error {e.status_code}: {e}")
```

## Idempotency

`sms.send()` and `email.send()` automatically generate a UUID `Idempotency-Key` header for every request.

## Requirements

- Python 3.10+
