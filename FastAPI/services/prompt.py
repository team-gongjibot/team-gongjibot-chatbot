# def build_prompt(question: str, docs: list):
#     context = "\n\n".join([f"[{doc['title']}]\n{doc['text']}" for doc in docs])
#     return f"""[문서 기반 Q&A]
# 질문: {question}
# 문서:
# {context}
#
#답변:"""

def build_prompt(question: str, docs: list):
    context = "\n\n".join([f"[{doc['title']}]\n{doc['text']}" for doc in docs])
    notice_text = """
맥락 : "{context}"


질문 : {question}
    """
    print(notice_text.format(context = context, question=question)[:100])
    print(f"질문 : {question}")
    
    return notice_text.format(context = context, question=question)

