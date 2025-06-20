import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.embedding import embed_question
from utils.vector_search import search_similar_docs
from services.prompt import build_prompt
from services.prompt import is_invailed_response
from services.llm import generate_answer

url = "https://vervet-upright-pony.ngrok-free.app/ask"
headers = {"Content-Type": "application/json"}

# 테스트할 질문 예시
data = {
    "text": "부처님오신날로 인한 보강 날짜가 언제야?"
}


try:
    question = "안녕"
    q_embedding = embed_question(question)
    count = 0
    while(True):
    
        related_docs = search_similar_docs(q_embedding,count)
        
        prompt = build_prompt(question,related_docs)
        answer = generate_answer(prompt)
        print(answer)
        if is_invailed_response(answer):
            count+=1
        else:
            break
    
    print(answer)
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

'''
try:
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        res_json = response.json()
        print("✅ 응답 성공!")
        print("답변:", res_json.get("answer"))
        print("참조 문서:")
        for doc in res_json.get("source_docs", []):
            print(f" - {doc['id']}: {doc['title']}")
    else:
        print("❌ 상태 코드:", response.status_code)
        print("⚠️ 응답 내용:", response.text)
except Exception as e:
    print("❌ 요청 실패:", e)
'''