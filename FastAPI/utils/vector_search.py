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

with open("final_dataset.json","r",encoding="utf-8") as f:
    data = json.load(f)
df=pd.DataFrame(data)

df["tokenize_doc"] = df["summary"].apply(lambda x: x.split())

dimension = len(df["embedding"][0])
index = faiss.IndexFlatL2(dimension)
doc_embeddings = np.stack(df["embedding"].values)
index.add(doc_embeddings)


def search_similar_docs(vector, Index):
    if Index >= 10:
        return False
    vector = np.array([vector]).astype('float32')
    scores, indices = index.search(vector, 10)
    
    # print("\n\n\n")
    # for i in range(5):
    #     print(f"{i+1}위 문서 : {df.loc[indices[0][i], 'summary']} \n (거리 : {scores[0][i]:.4f}) (인덱스 : {indices[0][i]})")
    # print("\n\n\n")
        
    docs = df.loc[indices[0][Index], "summary"]
    print(docs)
    
    return docs
