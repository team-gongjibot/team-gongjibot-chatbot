# ✅ OpenAI 최신 버전 방식으로 설정
from openai import OpenAI

# LM Studio API 서버 연결
client = OpenAI(
    base_url="http://localhost:1234/v1",  # LM Studio 주소
    api_key="lm-studio"  # 아무 문자열도 OK
)


def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model="local-model",  # LM Studio 연결용
        messages=[
            {"role": "user", "content": prompt}  # 템플릿 적용된 전체 prompt를 user로 보냄
        ],
        temperature=0.2,
        max_tokens=1024,
        frequency_penalty=0.4,
        presence_penalty=0.1,
    )
    
    
    return response.choices[0].message.content.strip()

