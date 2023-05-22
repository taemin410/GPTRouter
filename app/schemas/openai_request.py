from typing import Optional
from pydantic import BaseModel


class RequestCompletion(BaseModel):
    prompt: str
    model_name: Optional[str]

class Message(BaseModel):
    role: str
    content: str

class RequestChat(BaseModel):
    messages: list[Message]