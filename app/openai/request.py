import logging
from fastapi import Depends, HTTPException
import openai
import requests

from app.config import get_settings
from app.schemas.kakao_response import KakaoChatbotResponse

logger = logging.getLogger(__name__)

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
    
    res = requests.post(url, json=KakaoChatbotResponse(version=2.0, template=template).json())

    if not res.ok:
        raise HTTPException(status_code=503, detail=f"Kakao POST {url} failed.")

    print(f"sent request successfully to kakao POST {url}, {res.status_code}")
    logger.info(res.json())