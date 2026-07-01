from src.openai_client import get_openai_client
from src.config import settings

def ask_llm(prompt: str) -> str:

    if settings.can_call_openai:
        return prompt
    
    client = get_openai_client()

    response = client.responses.create(
        model = settings.model,
        input = prompt
    )
    return response.output_text

