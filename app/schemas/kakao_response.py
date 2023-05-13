from typing import Optional
from pydantic import BaseModel


class SimpleText(BaseModel):
    text: str


class Output(BaseModel):
    simpleText: SimpleText


class Template(BaseModel):
    outputs: list[Output]


class KakaoChatbotResponse(BaseModel):
    version: str
    template: Template


class KakaoChatbotResponseCallback(BaseModel):
    version: str
    useCallback: bool
    template: Optional[Template]
