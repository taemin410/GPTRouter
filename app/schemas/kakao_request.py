from typing import Any

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
    params: dict[str, Any]
    detailParams: dict[str, Any]
    clientExtra: dict[str, Any]


class Block(BaseModel):
    id: str
    name: str


class Properties(BaseModel):
    botUserKey: str
    bot_user_key: str


class User(BaseModel):
    id: str
    type: str
    properties: Properties


class Params(BaseModel):
    ignoreMe: str
    surface: str


class UserRequest(BaseModel):
    block: Block
    user: User
    utterance: str
    params: Params
    lang: str
    timezone: str


class KakaoChatbotRequest(BaseModel):
    bot: Bot
    intent: Intent
    action: Action
    userRequest: UserRequest
    contexts: list
