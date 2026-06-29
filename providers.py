"""多 LLM Provider 注册表，全部走 OpenAI-compatible 接口"""

from dataclasses import dataclass, field


@dataclass
class ProviderConfig:
    id: str
    label: str
    endpoint: str
    models: list[dict] = field(default_factory=list)


PROVIDERS: list[ProviderConfig] = [
    ProviderConfig(
        id="deepseek",
        label="DeepSeek",
        endpoint="https://api.deepseek.com/v1",
        models=[
            {"id": "deepseek-chat", "label": "DeepSeek V3"},
            {"id": "deepseek-reasoner", "label": "DeepSeek R1"},
        ],
    ),
    ProviderConfig(
        id="openai",
        label="OpenAI",
        endpoint="https://api.openai.com/v1",
        models=[
            {"id": "gpt-4o", "label": "GPT-4o"},
            {"id": "gpt-4o-mini", "label": "GPT-4o Mini"},
        ],
    ),
    ProviderConfig(
        id="qwen",
        label="通义千问",
        endpoint="https://dashscope.aliyuncs.com/compatible-mode/v1",
        models=[
            {"id": "qwen-plus", "label": "Qwen Plus"},
            {"id": "qwen-max", "label": "Qwen Max"},
            {"id": "qwen-vl-plus", "label": "Qwen VL Plus"},
        ],
    ),
    ProviderConfig(
        id="glm",
        label="智谱 GLM",
        endpoint="https://open.bigmodel.cn/api/paas/v4",
        models=[
            {"id": "glm-4-plus", "label": "GLM-4 Plus"},
            {"id": "glm-4-flash", "label": "GLM-4 Flash"},
        ],
    ),
    ProviderConfig(
        id="moonshot",
        label="Kimi",
        endpoint="https://api.moonshot.cn/v1",
        models=[
            {"id": "moonshot-v1-8k", "label": "Moonshot v1 8K"},
            {"id": "moonshot-v1-32k", "label": "Moonshot v1 32K"},
        ],
    ),
    ProviderConfig(
        id="grok",
        label="Grok (xAI)",
        endpoint="https://api.x.ai/v1",
        models=[{"id": "grok-3", "label": "Grok 3"}],
    ),
    ProviderConfig(
        id="mistral",
        label="Mistral",
        endpoint="https://api.mistral.ai/v1",
        models=[{"id": "mistral-large-latest", "label": "Mistral Large"}],
    ),
]


def get_provider(provider_id: str) -> ProviderConfig | None:
    for p in PROVIDERS:
        if p.id == provider_id:
            return p
    return None


def get_model_list(provider_id: str) -> list[tuple[str, str]]:
    """返回 Gradio Dropdown 格式 [(label, id), ...]"""
    p = get_provider(provider_id)
    if not p:
        return []
    return [(m["label"], m["id"]) for m in p.models]
