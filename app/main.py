from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from sqlalchemy.exc import SQLAlchemyError

# from app.databases import db
# from app.routes.v1 import token, whitelist
from app.config import get_settings

import logging
import os


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

    configs = {
        "DB_URL": settings.db_url,
        "DB_POOL_RECYCLE": 900, # check pool cycle num
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


@app.get("/health-check", tags=["health_check"])
def health_check():
    return {"HealthCheck": True}


@app.get("/env", tags=["health_check"])
def health_check():
    env = os.environ.get("ENV")
    return {"Environment": env}
