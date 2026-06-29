"""数学题解答助手 — 桌面窗口版"""

import threading
import time
import sys
import os

import webview
import gradio as gr

# 确保工作目录正确
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import build_app, CSS, THEME


def start_gradio():
    """后台启动 Gradio 服务器"""
    app = build_app()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=False,
        css=CSS,
        theme=THEME,
        quiet=True,
    )


def main():
    # 后台启动 Gradio
    server_thread = threading.Thread(target=start_gradio, daemon=True)
    server_thread.start()

    # 等 Gradio 就绪
    import urllib.request
    for _ in range(30):
        try:
            urllib.request.urlopen("http://127.0.0.1:7860", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    else:
        print("Gradio 启动超时")
        sys.exit(1)

    # 打开原生桌面窗口
    webview.create_window(
        title="数学题解答助手",
        url="http://127.0.0.1:7860",
        width=1200,
        height=800,
        min_size=(900, 600),
        text_select=True,
    )
    webview.start()


if __name__ == "__main__":
    main()
