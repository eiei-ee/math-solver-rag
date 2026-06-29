"""数学题解答助手 — Gradio 入口"""

import gradio as gr

from config import Settings
from providers import PROVIDERS, get_model_list
from llm import stream_chat

_settings = Settings()

# 启动时同步初始化 RAG 索引（避免首次请求时构建导致超时）
from rag.retriever import init_index
init_index()


def on_provider_change(provider_id: str):
    """切换 Provider 时更新模型列表"""
    models = get_model_list(provider_id)
    return gr.Dropdown(choices=models, value=models[0][1] if models else None)


def chat_fn(
    message: str,
    history: list[dict],
    provider: str,
    model: str,
    api_key: str,
    temperature: float,
    use_rag: bool,
):
    """流式对话回调"""
    settings = Settings(
        provider=provider,
        model=model,
        api_key=api_key,
        temperature=temperature,
    )
    yield from stream_chat(
        message=message,
        history=history,
        settings=settings,
        use_rag=use_rag,
    )


CSS = """
footer { display: none !important; }
.gradio-container { max-width: 100% !important; }
"""

THEME = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="blue",
        neutral_hue="gray",
    ).set(
        body_background_fill="*neutral_50",
        body_background_fill_dark="*neutral_50",
        block_background_fill="white",
        block_background_fill_dark="white",
        block_label_text_color="*neutral_700",
        block_title_text_color="*neutral_800",
        body_text_color="*neutral_800",
        body_text_color_subdued="*neutral_600",
        border_color_primary="*neutral_300",
        button_primary_background_fill="*primary_500",
        button_primary_text_color="white",
    )


def build_app() -> gr.Blocks:
    with gr.Blocks(
        title="数学题解答助手",
        fill_height=True,
    ) as app:
        gr.Markdown("""# 数学题解答助手
基于 AI 大模型的数学题解题工具 — 逐步推导 · LaTeX 渲染 · RAG 知识库检索""")

        with gr.Row():
            with gr.Column(scale=3):
                provider_dd = gr.Dropdown(
                    choices=[(p.label, p.id) for p in PROVIDERS],
                    value=_settings.provider,
                    label="服务商",
                    interactive=True,
                )
                model_dd = gr.Dropdown(
                    choices=get_model_list(_settings.provider),
                    value=_settings.model,
                    label="模型",
                    interactive=True,
                )
                api_key_tb = gr.Textbox(
                    value=_settings.api_key,
                    label="API Key",
                    type="password",
                    placeholder="输入 API Key...",
                )
                temp_sl = gr.Slider(
                    minimum=0, maximum=2,
                    value=_settings.temperature, step=0.1,
                    label="温度 (Temperature)",
                )
                rag_cb = gr.Checkbox(
                    value=_settings.use_rag,
                    label="启用 RAG 知识库检索",
                )

                chat = gr.ChatInterface(
                    fn=chat_fn,
                    chatbot=gr.Chatbot(
                        height=550,
                        latex_delimiters=[
                            {"left": "$$", "right": "$$", "display": True},
                            {"left": "$", "right": "$", "display": False},
                            {"left": "\\[", "right": "\\]", "display": True},
                            {"left": "\\(", "right": "\\)", "display": False},
                        ],
                        show_label=False,
                    ),
                    additional_inputs=[
                        provider_dd, model_dd, api_key_tb, temp_sl, rag_cb
                    ],
                    additional_inputs_accordion=gr.Accordion("设置 (Settings)", open=False),
                    examples=[
                        ["解方程：x² - 5x + 6 = 0"],
                        ["求函数 f(x) = x³ - 3x² + 2 的单调区间和极值"],
                        ["计算 ∫₀¹ x·eˣ dx"],
                        ["证明：√2 是无理数"],
                    ],
                    title="",
                )

                provider_dd.change(
                    fn=on_provider_change,
                    inputs=[provider_dd],
                    outputs=[model_dd],
                )

            with gr.Column(scale=1):
                gr.Markdown("""### 使用说明
1. 展开「设置」填入 **API Key**
2. 选择服务商和模型
3. 输入数学题目并发送
4. AI 逐步推导解答

### 输入格式
- **文字**：直接输入题目
- **LaTeX**：用 `$...$` 或 `$$...$$` 包裹

### RAG 知识库
开启后从知识库检索相关公式定理：
- 代数 / 几何 / 三角
- 微积分 / 概率统计
- 线性代数 / 解析几何
- 高考考研真题

### 注意事项
- API Key 须有效且有余额
- 复杂题目响应时间更长
- 答案仅供参考，请自行验证
""")
                gr.ClearButton(
                    components=[chat.chatbot],
                    value="清空对话",
                    variant="secondary",
                )

    return app


if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
        css=CSS,
        theme=THEME,
    )
