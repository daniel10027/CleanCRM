from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class UserEntity:
    id: int
    email: str
    username: str
    is_active: bool

@dataclass
class OTPCode:
    id: int
    user_id: int
    code: str
    purpose: str  # "login" | "password_reset"
    expires_at: datetime
    used: bool