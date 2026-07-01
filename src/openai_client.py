from openai import OpenAI

from src.config import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.api_key)