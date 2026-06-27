from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self):
        self.api_key = self._get_required("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    @staticmethod
    def _get_required(key: str) -> str:
        value = os.getenv(key)

        if not value:
            raise ValueError(f"{key} not found.")

        return value


settings = Settings()