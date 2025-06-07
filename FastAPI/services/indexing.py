from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np
import json
import os

MODEL_NAME = "intfloat/multilingual-e5-base"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

def embed(text: str) -> np.ndarray:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # KoBERT는 token_type_ids를 지원하지 않거나 문제가 되므로 제거
    if "token_type_ids" in inputs:
        del inputs["token_type_ids"]

    with torch.no_grad():
        outputs = model(**inputs)

    return outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()


def build_faiss_index(json_path: str = None, index_path: str = None) -> dict:
    # 기본 경로: 현재 파일 기준 상위 디렉토리에 있는 announcements.json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = json_path or os.path.join(base_dir, "announcements.json")
    index_path = index_path or os.path.join(base_dir, "announcements.index")

    if not os.path.exists(json_path):
        return {"status": "error", "message": f"JSON file '{json_path}' not found."}

    with open(json_path, encoding="utf-8") as f:
        documents = json.load(f)

    if os.path.exists(index_path):
        return {"status": "skipped", "message": f"Index already exists at '{index_path}'."}

    embeddings = []
    seen_texts = set()
    for doc in documents:
        text = doc["text"]
        if text in seen_texts:
            continue
        seen_texts.add(text)
        emb = embed(text)
        embeddings.append(emb)

    if not embeddings:
        return {"status": "error", "message": "No unique documents found to index."}

    vectors = np.stack(embeddings).astype("float32")
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    faiss.write_index(index, index_path)

    return {"status": "success", "count": len(embeddings), "index_path": index_path}