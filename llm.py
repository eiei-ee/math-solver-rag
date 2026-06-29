"""LangChain LLM 对话链 — 流式 Chat + RAG 检索增强"""

from typing import Generator

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from config import Settings
from providers import get_provider
from prompts import build_full_prompt
from rag.retriever import retrieve_context


def create_llm(settings: Settings) -> ChatOpenAI:
    """根据配置创建 ChatOpenAI 实例（兼容所有 OpenAI 接口的 Provider）"""
    provider = get_provider(settings.provider)
    base_url = provider.endpoint if provider else "https://api.deepseek.com/v1"

    return ChatOpenAI(
        model=settings.model,
        api_key=settings.api_key,
        base_url=base_url,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        streaming=True,
        request_timeout=30,
    )


def build_messages(
    history: list[dict],
    system_prompt: str,
) -> list:
    """将 Gradio 聊天历史转为 LangChain 消息列表"""
    messages = [SystemMessage(content=system_prompt)]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    return messages


def stream_chat(
    message: str,
    history: list[dict],
    settings: Settings,
    use_rag: bool = True,
    input_type: str = "text",
) -> Generator[str, None, None]:
    """流式对话生成器，Gradio ChatInterface 直接消费"""

    # 1. RAG 检索
    rag_context = ""
    if use_rag:
        try:
            rag_context = retrieve_context(message, k=5)
        except Exception as e:
            rag_context = f"[知识库检索失败: {e}]"

    # 2. 构建 system prompt
    system_prompt = build_full_prompt(
        input_type=input_type,
        rag_context=rag_context,
    )

    # 3. 构建消息
    messages = build_messages(history, system_prompt)
    messages.append(HumanMessage(content=message))

    # 4. 创建 LLM 并流式调用
    try:
        llm = create_llm(settings)
        full_response = ""
        yield "思考中..."
        for chunk in llm.stream(messages):
            if chunk.content:
                if full_response == "思考中...":
                    full_response = ""
                full_response += chunk.content
                yield full_response
    except Exception as e:
        yield f"**错误**: {_format_error(e)}"


def _format_error(e: Exception) -> str:
    """格式化异常信息为用户友好提示"""
    msg = str(e)
    if "401" in msg or "Unauthorized" in msg or "Invalid API Key" in msg:
        return "API Key 无效，请在设置中检查。"
    if "402" in msg or "Insufficient Balance" in msg:
        return "API 余额不足，请充值后重试。"
    if "429" in msg or "Rate limit" in msg:
        return "请求过于频繁，请稍后重试。"
    if "timeout" in msg.lower() or "timed out" in msg.lower():
        return "请求超时，请检查网络连接后重试。"
    if "Connection" in msg:
        return "网络连接失败，请检查网络或 API 地址是否正确。"
    return f"请求失败：{msg}"
