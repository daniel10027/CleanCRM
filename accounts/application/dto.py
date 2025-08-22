from dataclasses import dataclass
from typing import Callable

@dataclass
class RegisterDTO:
    email: str
    username: str
    password: str

@dataclass
class LoginDTO:
    username: str
    password: str

@dataclass
class PasswordResetRequestDTO:
    email: str

@dataclass
class PasswordResetConfirmDTO:
    user_id: int
    code: str
    change_password: Callable[[], None]