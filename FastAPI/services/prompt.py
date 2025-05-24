def build_prompt(question: str, docs: list):
    context = "\n\n".join([f"[{doc['title']}]\n{doc['text']}" for doc in docs])
    return f"""[문서 기반 Q&A]
질문: {question}
문서:
{context}

답변:"""
