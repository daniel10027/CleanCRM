from typing import Protocol

class EmailSender(Protocol):
    def send(self, to_email: str, subject: str, body: str) -> None: ...

class SMSSender(Protocol):
    def send(self, to_phone: str, body: str) -> None: ...

class WhatsAppSender(Protocol):
    def send(self, to_phone: str, body: str) -> None: ...