import faiss
import numpy as np
import json
import pandas as pd

# 사전 구축된 인덱스 및 문서 리스트 로딩
#index = faiss.read_index("announcements.index")
#with open("announcements.json", encoding="utf-8") as f:
#    documents = json.load(f)

def get_doc_by_index(idx):
    return data[idx]

with open("data.json","r",encoding="utf-8") as f:
    data = json.load(f)
df=pd.DataFrame(data)

df["tokenize_doc"] = df["summary"].apply(lambda x: x.split())

dimension = len(df["embedding"][0])
index = faiss.IndexFlatL2(dimension)
doc_embeddings = np.stack(df["embedding"].values)
index.add(doc_embeddings)


def search_similar_docs(vector, top_k=3):
    vector = np.array([vector]).astype('float32')
    scores, indices = index.search(vector, top_k)
    
    result = []
    for i in indices[0]:
        if i == -1:
            continue
        try:
            result.append(get_doc_by_index(i))
        except IndexError:
            print(f"경고: FAISS 인덱스 {i}가 announcements.json 범위를 벗어났습니다.")
    
    return result
