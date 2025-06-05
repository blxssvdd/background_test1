from typing import Optional

from pydantic import BaseModel


class UserModel(BaseModel):
    login: str
    password: str



class MessageModel(BaseModel):
    id: int
    send_mail: str
    incoming: Optional[str] = None
    user_id: int