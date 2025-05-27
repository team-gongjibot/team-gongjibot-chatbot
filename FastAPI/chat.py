from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.embedding import embed_question
from utils.vector_search import search_similar_docs
from services.prompt import build_prompt
from services.llm import generate_answer

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
        related_docs = search_similar_docs(q_embedding)
        
        prompt = build_prompt(question.text, related_docs)
        answer = generate_answer(prompt)

        return {
            "answer": answer,
            "source_docs": [
                {
                    "id": d["id"],
                    "title": d["title"]
                } for d in related_docs
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
