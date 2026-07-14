from dataclasses import dataclass


@dataclass
class SendSMSResponse:
    message_id: str
    to: str
    sender_name: str
    parts: int
    cost: float
    currency: str
    status: str


@dataclass
class SendEmailResponse:
    message_id: str
    status: str


@dataclass
class MessageStatusResponse:
    id: str
    to: str
    sender_name: str
    parts: int
    cost: float
    status: str
    created_at: str
    sent_at: str | None = None
    delivered_at: str | None = None
    error: str | None = None


@dataclass
class BalanceResponse:
    available_balance: float
    current_balance: float
    currency: str
