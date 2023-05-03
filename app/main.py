from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError
from fastapi.responses import JSONResponse
import openai
from app.config import get_settings

import logging
import os

from app.openai.request import create_completion_request
from app.schemas.openai_request import RequestCompletion
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


@app.post("/chatgpt", tags=["openai"], response_model=ResponseCompletion)
def make_chatgpt_request_to_openai(completion_request: RequestCompletion):
    # @TODO: Handle model name param
    return ResponseCompletion(
        completion=create_completion_request(prompt=completion_request.prompt)
    )


@app.get("/health-check", tags=["health_check"])
def health_check():
    return {"HealthCheck": True}


@app.get("/env", tags=["health_check"])
def health_check():
    env = os.environ.get("ENV")
    return {"Environment": env}
