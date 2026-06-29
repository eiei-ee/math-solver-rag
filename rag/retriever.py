"""TF-IDF 向量化 + 余弦相似度检索 — 纯离线"""

import threading
from pathlib import Path
import pickle

import numpy as np
from scipy.sparse import csr_matrix, save_npz, load_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .loader import load_knowledge_documents, split_documents

CACHE_DIR = Path(__file__).parent.parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)
PKL_PATH = CACHE_DIR / "vectorizer.pkl"
NPZ_PATH = CACHE_DIR / "tfidf_matrix.npz"
TEXTS_PATH = CACHE_DIR / "texts.pkl"

_lock = threading.Lock()


def _build_index():
    """构建 TF-IDF 索引，用 npz 存矩阵（比 pickle 快 10x）"""
    docs = load_knowledge_documents()
    chunks = split_documents(docs)
    texts = [c.page_content for c in chunks]
    metadatas = [c.metadata for c in chunks]

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(1, 3),
        max_features=5000,
    )
    matrix = vectorizer.fit_transform(texts)

    # 分开存储：vectorizer 用 pickle，矩阵用 npz（快速），texts 用 pickle
    with open(PKL_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    save_npz(str(NPZ_PATH), matrix)
    with open(TEXTS_PATH, "wb") as f:
        pickle.dump((texts, metadatas), f)

    return {"vectorizer": vectorizer, "matrix": matrix, "texts": texts, "metadatas": metadatas}


def _load_index():
    """加载缓存"""
    if PKL_PATH.exists() and NPZ_PATH.exists() and TEXTS_PATH.exists():
        with open(PKL_PATH, "rb") as f:
            vectorizer = pickle.load(f)
        matrix = load_npz(str(NPZ_PATH))
        with open(TEXTS_PATH, "rb") as f:
            texts, metadatas = pickle.load(f)
        return {"vectorizer": vectorizer, "matrix": matrix, "texts": texts, "metadatas": metadatas}
    return _build_index()


_index = None


def init_index():
    """启动时调用，同步初始化（线程安全）"""
    global _index
    with _lock:
        if _index is None:
            _index = _load_index()


def get_index():
    if _index is None:
        init_index()
    return _index


def retrieve_context(query: str, k: int = 5) -> str:
    """TF-IDF 检索 Top-K 文档片段"""
    idx = get_index()
    query_vec = idx["vectorizer"].transform([query])
    sims = cosine_similarity(query_vec, idx["matrix"])[0]
    top_k = sims.argsort()[-k:][::-1]

    lines = []
    seen = set()
    count = 0
    for i in top_k:
        if sims[i] <= 0:
            continue
        text = idx["texts"][i]
        key = text[:60]
        if key in seen:
            continue
        seen.add(key)
        count += 1
        src = Path(idx["metadatas"][i].get("source", "")).name
        lines.append(f"[参考{count}] ({src})\n{text}")

    return "\n\n---\n\n".join(lines)
