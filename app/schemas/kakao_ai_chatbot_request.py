from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Bot(BaseModel):
    id: str
    name: str


class Reason(BaseModel):
    code: int
    message: str


class Extra(BaseModel):
    reason: Reason


class Intent(BaseModel):
    id: str
    name: str
    extra: Extra


class Action(BaseModel):
    id: str
    name: str
    params: Dict[str, Any]
    detailParams: Dict[str, Any]
    clientExtra: Dict[str, Any]


class Block(BaseModel):
    id: str
    name: str


class Properties(BaseModel):
    botUserKey: str
    plusfriendUserKey: str
    bot_user_key: str
    plusfriend_user_key: str


class User(BaseModel):
    id: str
    type: str
    properties: Properties


class Params(BaseModel):
    surface: str


class UserRequest(BaseModel):
    block: Block
    user: User
    utterance: str
    params: Params
    callbackUrl: str
    lang: str
    timezone: str


class KakaoAIChatbotRequest(BaseModel):
    bot: Optional[Bot] = None
    intent: Optional[Intent] = None
    action: Optional[Action] = None
    userRequest: Optional[UserRequest] = None
    contexts: Optional[List] = None
