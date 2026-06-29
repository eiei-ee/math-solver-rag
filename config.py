import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    provider: str = os.getenv("PROVIDER", "deepseek")
    api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    temperature: float = 0.7
    max_tokens: int = 4096
    use_rag: bool = True
