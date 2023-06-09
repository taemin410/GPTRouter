from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError
from fastapi.responses import JSONResponse
import openai
from app.config import get_settings

import logging
import os

from app.openai.request import create_callback_request_kakao, create_chat_request, create_completion_request
from app.schemas.kakao_ai_chatbot_request import KakaoAIChatbotRequest
from app.schemas.kakao_request import KakaoChatbotRequest
from app.schemas.kakao_response import KakaoChatbotResponse, KakaoChatbotResponseCallback, SimpleText
from app.schemas.openai_request import RequestChat, RequestCompletion
from app.schemas.openai_response import ResponseCompletion


def init_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def start_app():
    settings = get_settings()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    configs = {
        "DB_URL": settings.db_url,
        "DB_POOL_RECYCLE": 900,  # check pool cycle num
        "DB_ECHO": False,
    }

    tags_metadata = [
        {
            "name": "v1",
            "description": "version 1 APIs",
        },
    ]

    app = FastAPI(openapi_tags=tags_metadata)

    # app.include_router(router.router)

    # @TODO: allow origins from our Domain
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # db.init_app(app, **configs)

    return app


init_logging()

# init app
app = start_app()


# @app.exception_handler(SQLAlchemyError)
# async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
#     return JSONResponse(
#         status_code=500,
#         content={"message": f"Oops! {exc}"},
#     )

@app.exception_handler(OpenAIError)
async def openai_exception_handler(request: Request, exc: OpenAIError):
    return JSONResponse(
        status_code=503,
        content={"message": f"Oops! OpenAI API request failed: {exc} "},
    )


@app.post("/model", tags=["openai"])
async def set_model_name(model_name: str):
    get_settings().model_name = model_name
    return get_settings().model_name


@app.post("/max-tokens", tags=["openai"])
async def set_max_tokens(max_tokens: int):
    get_settings().max_tokens = max_tokens
    return get_settings().max_tokens


@app.post("/chat-completion", tags=["openai"], response_model=SimpleText)
async def make_chatgpt_chat_request(chat_request: RequestChat):

    completion = await create_chat_request(messages=chat_request.messages)
    return SimpleText(text=completion)


@app.post("/completion", tags=["openai"], response_model=ResponseCompletion)
async def make_chatgpt_completion_request_v2(completion_request: RequestCompletion):
    completion = await create_completion_request(prompt=completion_request.prompt)
    return ResponseCompletion(
        completion=completion
    )


@app.post("/chatgpt", tags=["openai"], response_model=ResponseCompletion)
async def make_chatgpt_completion_request(completion_request: RequestCompletion):
    completion = await create_completion_request(prompt=completion_request.prompt)
    return ResponseCompletion(
        completion=completion
    )


@app.post("/api/chat", tags=["kakao"], response_model=KakaoChatbotResponse)
async def make_chatgpt_request_to_openai_from_kakao(completion_request: KakaoChatbotRequest):
    completion = await create_completion_request(prompt=completion_request.userRequest.utterance)
    # erase newline
    completion = completion.strip()
    template = {
        "outputs": [
            {"simpleText": {"text": completion}}
        ]
    }
    return KakaoChatbotResponse(version="2.0", template=template)


@app.post("/api/chat/callback", tags=["kakao"], response_model=KakaoChatbotResponseCallback)
async def make_chatgpt_async_callback_request_to_openai_from_kakao(
        kakao_ai_request: KakaoAIChatbotRequest,
        background_tasks: BackgroundTasks):

    background_tasks.add_task(create_callback_request_kakao,
                              prompt=kakao_ai_request.userRequest.utterance, url=kakao_ai_request.userRequest.callbackUrl)
    return KakaoChatbotResponseCallback(version="2.0", useCallback=True)


@app.get("/health-check", tags=["health_check"])
def health_check():
    return {"HealthCheck": True}


@app.get("/env", tags=["health_check"])
def health_check():
    env = os.environ.get("ENV")
    return {"Environment": env}
