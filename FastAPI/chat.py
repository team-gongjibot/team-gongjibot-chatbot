from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.embedding import embed_question
from utils.vector_search import search_similar_docs
from services.prompt import build_prompt
from services.prompt import is_invailed_response
from services.llm import generate_answer
import re

app = FastAPI()

class Question(BaseModel):
    text: str

@app.get("/ping")
async def ping():
    return {"status": "pong"}

@app.post("/ask")
async def ask_question(question: Question):
    try:
        q_embedding = embed_question(question.text)
        count = 0
        while(True):
        
            related_docs = search_similar_docs(q_embedding,count)
            
            if related_docs == False:
                answer = "질문에 관한 정보가 너무 적습니다. 질문을 구체화 해서 다시 질문해주세요."
                break
            
            prompt = build_prompt(question.text,related_docs)
            answer = generate_answer(prompt)

            print(answer)
            if is_invailed_response(answer):
                count+=1
            else:
                break
        answer = re.sub(r"[\s\S]*?</think>", "", answer)
        answer = re.sub(r'<think>', '', answer, flags=re.DOTALL)
        answer = re.sub(r'#', '', answer, flags=re.DOTALL)
        return {
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))