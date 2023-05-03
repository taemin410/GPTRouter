from fastapi import Depends
import openai

from app.config import get_settings


async def create_completion_request(prompt: str, model_name: str = "text-davinci-003") -> str:
    settings = get_settings()

    completion = await openai.Completion.acreate(
        model=model_name, prompt=prompt, max_tokens=settings.max_tokens)

    # Get the completion text from the first choice in the choices list
    text = completion.choices[0]["text"]

    return text
