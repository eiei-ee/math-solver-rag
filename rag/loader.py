"""文档加载与文本切分"""

from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def load_knowledge_documents() -> list:
    """加载 knowledge/ 下所有 .md 文件"""
    loader = DirectoryLoader(
        str(KNOWLEDGE_DIR),
        glob="**/*.md",
        loader_cls=lambda path: TextLoader(str(path), encoding="utf-8"),
        show_progress=True,
    )
    return loader.load()


def split_documents(docs: list) -> list:
    """RecursiveCharacterTextSplitter 中文友好的分块"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""],
    )
    return splitter.split_documents(docs)
