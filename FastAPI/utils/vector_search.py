import faiss
import numpy as np
import json

# 사전 구축된 인덱스 및 문서 리스트 로딩
index = faiss.read_index("announcements.index")
with open("announcements.json", encoding="utf-8") as f:
    documents = json.load(f)

def get_doc_by_index(idx):
    return documents[idx]

def search_similar_docs(vector, top_k=3):
    vector = np.array([vector]).astype('float32')
    scores, indices = index.search(vector, top_k)
    return [get_doc_by_index(i) for i in indices[0] if i != -1]
