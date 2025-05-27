# ✅ OpenAI 최신 버전 방식으로 설정
from openai import OpenAI

# LM Studio API 서버 연결
client = OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio 주소
    api_key="lm-studio"  # 아무 문자열도 OK
)


def generate_answer(prompt: str, max_new_tokens: int = 128) -> str:
    system_prompt = """
당신은 제공된 맥락에 따라 질문에 답하는 유용한 AI입니다. 반드시 한국어로 답 해주세요.
"""

    response = client.chat.completions.create(
        model="local-model",  # LM Studio에서 실행 중인 모델 (이름은 무시됨)
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1024,
        frequency_penalty=0.4,
        presence_penalty=0.1,
    )
    
    
    return response.choices[0].message.content.strip()

