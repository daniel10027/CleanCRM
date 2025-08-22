from dataclasses import dataclass
from typing import Literal

Channel = Literal["email","sms","whatsapp"]

@dataclass
class CampaignEntity:
    id: int
    name: str
    channel: Channel
    subject: str | None
    body: str
    directory_id: int