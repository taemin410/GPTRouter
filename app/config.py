from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    db_url: str = "mysql://root:password@db/test"  # default set to local mysql
    web_hook_url: str = "https://discord.com/api/webhooks/970181039395844136/7iJmxKZ2DKgSl3Bf8uimcES8BqHGki1l_S4mawbFZZhcsKexPx-mL0XkJo-7ZDRVAyzO"  # Test url


@lru_cache()
def get_settings() -> Settings:
    return Settings()
