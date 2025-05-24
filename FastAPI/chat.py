from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.embedding import embed_question
from utils.vector_search import search_similar_docs
from services.prompt import build_prompt
from services.llm import generate_answer

router = APIRouter()

class Question(BaseModel):
    text: str

@router.post("/ask")
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
