import logging
from fastapi import Depends, HTTPException
import openai
import requests

from app.config import get_settings
from app.schemas.kakao_response import KakaoChatbotResponse
from app.schemas.openai_request import Message

logger = logging.getLogger(__name__)

NUMBER_OF_CHAT_HISTORY = 5
TEMPERATURE = 0.7

async def create_completion_request(prompt: str) -> str:
    settings = get_settings()

    completion = await openai.Completion.acreate(
        model=settings.model_name, prompt=prompt, max_tokens=settings.max_tokens)

    # Get the completion text from the first choice in the choices list
    text = completion.choices[0]["text"]

    return text


async def create_callback_request_kakao(prompt: str, url: str) -> dict:

    completion_text = await create_completion_request(prompt)
    template = {
        "outputs": [
            {"simpleText": {"text": completion_text}}
        ]
    }

    res = requests.post(url, json=KakaoChatbotResponse(
        version="2.0", template=template).json())

    if not res.ok:
        raise HTTPException(
            status_code=503, detail=f"Kakao POST {url} failed.")

    print(f"sent request successfully to kakao POST {url}, {res.status_code}")
    logger.info(res.json())


async def create_chat_request(messages: list[Message]) -> str:
    settings = get_settings()

    messages_base = [
        {
            "role" : 'system',
            "content" : """An AI assistant that is a medical expert in emergency and hospitals have an inspiring and humorous conversation.
            AI assistant is a brand new, powerful, human-like artificial intelligence.
            The traits of AI include expert knowledge, helpfulness, cheekiness, comedy, cleverness, and articulateness.
            AI is a well-behaved and well-mannered individual.
            AI is always friendly, kind, and inspiring, and he is eager to provide vivid and thoughtful responses to the user.
            AI has the sum of all knowledge in their brain, and is able to accurately answer nearly any question about any topic in conversation.
            AI is going to serve clients with both Korean and English queries"""
        }
    ]

    last_n_messages = messages[-NUMBER_OF_CHAT_HISTORY:]
    joined_messages = messages_base + [msg.dict() for msg in last_n_messages]

    chat_completion = await openai.ChatCompletion.acreate(

        model=settings.chat_model_name,
        messages=joined_messages,
        temperature=TEMPERATURE,
        max_tokens=settings.max_tokens)

    # Get the chat completion text from the first choice in the choices list
    text = chat_completion.choices[0]["message"]["content"]

    return text
