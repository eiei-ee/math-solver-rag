# 数学题解答助手：Python RAG 原型

本仓保留数学助手系列的 Python 检索与提示词原型。当前主维护应用为 [math-solver-unified](https://github.com/eiei-ee/math-solver-unified)，已经将检索和提示词行为迁移为 TypeScript；新用户请优先查看该仓。

## 本地运行历史原型

在 Python 虚拟环境中安装 `requirements.txt`，再启动 Gradio 界面：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

打开 `http://127.0.0.1:7860`，在设置中选择服务商、模型并输入自己的 API Key。界面仅绑定本机，模型请求会发送给所选服务商并可能产生费用。依赖版本未完全锁定，本原型未在本次整理中重新验证所有第三方 API。

`desktop_app.py` 是可选的 pywebview 包装入口，另需安装 `pywebview`；它不是 `requirements.txt` 中默认安装的组件。

## 内容和权利边界

检索使用本地 Markdown、TF-IDF 和余弦相似度。知识资料需要继续审校；历史考试题若没有明确年份、题号、来源和再分发依据，不应作为可信答案或再次打包分发。

本仓暂不授予开源许可证，保留权利；详见 [RIGHTS.md](RIGHTS.md)。源码历史保留用于溯源。
