# def build_prompt(question: str, docs: list):
#     context = "\n\n".join([f"[{doc['title']}]\n{doc['text']}" for doc in docs])
#     return f"""[문서 기반 Q&A]
# 질문: {question}
# 문서:
# {context}
#
#답변:"""
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
model = SentenceTransformer("intfloat/multilingual-e5-base")

def build_prompt(query: str, doc) -> str:
    target_notice = doc

    # ChatML 템플릿 적용
    messages = [
        {"role": "system", "content": 
            """당신은 검색 기반 질문응답을 지원하는 친절하고 이성적인 챗봇입니다. 당신의 임무는 다음과 같습니다:

1. 사용자의 질문을 정확히 이해하고, 필요한 경우 외부 검색 또는 문서 기반 정보를 활용해 정답을 추론합니다.
2. 불확실한 정보는 추측하지 말고, 필요한 경우 "질문과 관련된 정보는 제공된 맥락에 포함되어 있지 않습니다."라고만 출력하고, 그 외의 내용은 답변에 포함시키지 마세요요.
3. 응답은 명확하고 간결하며, 친절한 말투로 작성하세요.
4. 특정 질문에는 검색 API 또는 벡터DB를 활용하여 최신 정보를 반영하세요.
6. 절대 허위 정보는 생성하지 말고, 출처가 불확실한 경우 "질문과 관련된 정보는 제공된 맥락에 포함되어 있지 않습니다."라고만 출력하고, 그 외의 내용은 답변에 포함시키지 마세요요..
"""

        },
        {"role": "user", "content": f"맥락:{target_notice}\n\n질문: {query}"}
    ]

    # tokenizer로 ChatML 템플릿 적용
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True  # assistant 시작 토큰을 추가해야 모델이 응답을 생성
    )
    return prompt

def is_invailed_response(response):

    if "정보 없음" in response:
        return True
    import numpy as np
    from scipy.spatial.distance import euclidean

    text_embedding = model.encode(response, convert_to_numpy=True)

    invailed_doc_text = f"질문과 관련된 정보는 제공된 맥락에 포함되어 있지 않습니다."
    invailed_doc= model.encode(invailed_doc_text,convert_to_numpy=True)
    
    embedding1 = np.array(text_embedding)
    embedding2 = np.array(invailed_doc)
    
    dist = euclidean(embedding1, embedding2)
    print(dist)
    if dist <0.5:
        return True
    else:
        return False